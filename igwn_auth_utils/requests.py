# -*- coding: utf-8 -*-
# Copyright 2021 Cardiff University
# Distributed under the terms of the BSD-3-Clause license

"""Python Requests interface with IGWN authentication

This is heavily inspired by Leo Singer's excellent
:mod:`requests_gracedb` package.
"""

__author__ = "Duncan Macleod <duncan.macleod@ligo.org>"
__credits__ = "Leo Singer <leo.singer@ligo.org>"

from urllib.parse import urlparse

from safe_netrc import netrc

import requests

from . import (
    IgwnAuthError,
    find_scitoken,
    find_x509_credentials,
    scitoken_authorization_header,
)

_auth_session_parameters = """
    Discovery/configuration of authorisation/authentication methods
    is attempted in the following order:

    1.  if ``force_noauth=True`` is given, no auth is configured;

    2.  if a bearer token is provided via the ``token`` keyword argument,
        then use that;

    3.  if an X.509 credential path is provided via the ``cert`` keyword
        argument, then use that;

    4.  if ``auth`` keyword is provided, then use that;

    5.  look for a bearer token by passing the ``token_audience``
        and ``token_scope`` keyword parameters to
        :func:`igwn_auth_utils.find_scitokens`;

    6.  look for an X.509 credential using
        :func:`igwn_auth_utils.find_x509_credential`

    7.  read the netrc file located at :file:`~/.netrc`, or at the path
        stored in the :envvar:`NETRC` environment variable, and look
        for a username and password matching the hostname given in the
        ``url`` keyword argument;

    8.  if none of the above yield a credential, and ``fail_if_noauth=True``
        was provided, raise a `ValueError`.

    Parameters
    ----------
    token : `scitokens.SciToken`, `str`, `bool`, optional
        Bearer token (scitoken) input, one of

        - a bearer token (`scitokens.SciToken`),
        - a serialised token (`str`, `bytes`),
        - `False`: disable using tokens completely
        - `True`: discover a valid token via
          :func:`igwn_auth_utils.find_scitoken` and
          error if something goes wrong
        - `None`: try and discover a valid token, but
          try something else if that fails

    token_audience, token_scope : `str`
        The ``audience`` and ``scope`` to pass to
        :func:`igwn_auth_utils.find_scitoken` when discovering
        available tokens.

    cert : `str`, `tuple`, `bool`, optional
        X.509 credential input, one of

        - path to a PEM-format certificate file,
        - a ``(cert, key)`` `tuple`,
        - `False`: disable using X.509 completely
        - `True`: discover a valid cert via
          :func:`igwn_auth_utils.find_x509_credentials` and
          error if something goes wrong
        - `None`: try and discover a valid cert, but
          try something else if that fails

    auth :  `tuple`, `object`, optional
        ``(username, password)`` `tuple` or other authentication/authorization
        object to attach to a `~requests.Request`

    url : `str`, optional
        the URL that will be queried within this session; this is only
        used to access credentials via :mod:`safe_netrc`.

    force_noauth : `bool`, optional
        Disable the use of any authorisation credentials (mainly for testing).

    fail_if_noauth : `bool`, optional
        Raise a `~igwn_auth_utils.IgwnAuthError` if no authorisation
        credentials are presented or discovered.

    Raises
    ------
    IgwnAuthError
        If ``cert=True`` or ``token=True`` is given and the relevant
        credential was not actually discovered, or
        if ``fail_if_noauth=True`` is given and no authorisation
        token/credentials of any valid type are presented or discovered.

    Note
    ----
    This class requires `Requests <https://requests.readthedocs.io/>`__.

    See also
    --------
    requests.Session
        for details of the standard options
    """.strip()


def _find_cred(func, *args, error=True, **kwargs):
    """Find a credential and maybe ignore an `~igwn_auth_utils.IgwnAuthError`

    This is an internal utility for the `SessionAuthMixin._init_auth`
    method which shouldn't necessary fail if it doesn't
    find a credential of any one type, but should just move on to the
    next option.
    """
    try:
        return func(*args, **kwargs)
    except IgwnAuthError:
        if error:
            raise
        return


def _hook_raise_for_status(response, *args, **kwargs):
    """Response hook to raise exception for any HTTP error (status >= 400)

    Reproduced (with permission) from :mod:`requests_gracedb.errors`,
    authored by Leo Singer.
    """
    return response.raise_for_status()


class SessionErrorMixin:
    """A mixin for :class:`requests.Session` to raise exceptions for HTTP
    errors.

    Reproduced (with permission) from :mod:`requests_gracedb.errors`,
    authored by Leo Singer.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hooks.setdefault("response", []).append(
            _hook_raise_for_status,
        )


class SessionAuthMixin:
    """Mixin for :class:`requests.Session` to add support for IGWN auth.

    By default this mixin will automatically attempt to discover/configure
    a bearer token (scitoken) or an X.509 credential, with options to
    require/disable either of those, or all authentication entirely.

    {parameters}
    """
    def __init__(
        self,
        token=None,
        token_audience=None,
        token_scope=None,
        cert=None,
        auth=None,
        url=None,
        force_noauth=False,
        fail_if_noauth=False,
        **kwargs,
    ):
        # initialise session
        super().__init__(**kwargs)

        # handle options
        if force_noauth and fail_if_noauth:
            raise ValueError(
                "cannot select both force_noauth and fail_if_noauth",
            )
        if force_noauth:
            return

        # find creds if we can
        _auth = self._init_auth(
            auth=auth,
            cert=cert,
            token=token,
            token_audience=token_audience,
            token_scope=token_scope,
            url=url,
        )

        # if no auth was found, and we need it, fail here
        if not _auth and fail_if_noauth:
            raise IgwnAuthError("no valid authorisation credentials found")

    def _init_auth(
        self,
        auth=None,
        cert=None,
        token=None,
        token_audience=None,
        token_scope=None,
        url=None,
    ):
        # -- user-provided objects
        # the user gave us something specific, so always use it
        dummy = (None, False, True)
        if token not in dummy:
            return self._set_token_header(token)

        for attr, obj in (
                ("cert", cert),
                ("auth", auth),
        ):
            if obj not in dummy:
                setattr(self, attr, obj)
                return getattr(self, attr)

        # -- the user didn't give us something specific,
        #    so we go around the houses trying to find something
        #    we can use

        # bearer token
        if token is not False:  # not disabled
            token = self._find_token(
                token_audience,
                token_scope,
                error=bool(token),
            )
        if token:
            return self._set_token_header(token)

        # cert auth
        if cert is not False:  # not disabled
            self.cert = self._find_x509_credentials(error=bool(cert))
        if self.cert:
            return self.cert

        # basic auth (netrc)
        if auth is not False:  # not disabled
            self.auth = self._find_username_password(url)

        return self.auth

    def _set_token_header(self, token):
        """Serialise a `scitokens.SciToken` and format and store as an
        Authorization header for this session.

        Parameters
        ----------
        token : `scitokens.SciToken`, `str`, `bytes`
            the token to serialize, or an already serialized representation
        """
        if isinstance(token, (str, bytes)):  # load a valid token
            header = f"Bearer {token}"
        else:
            header = scitoken_authorization_header(token)
        self.headers["Authorization"] = header
        return header

    @staticmethod
    def _find_x509_credentials(error=True):
        """Find an X.509 certificate for authorization
        """
        return _find_cred(find_x509_credentials, error=error)

    @staticmethod
    def _find_token(audience, scope, error=True):
        """Find a bearer token for authorization
        """
        return _find_cred(find_scitoken, audience, scope, error=error)

    @staticmethod
    def _find_username_password(url):
        """Use `safe_netrc.netrc` to find the username/password for basic auth
        """
        host = urlparse(url).hostname

        try:
            result = netrc().authenticators(host)
        except IOError:
            return

        try:
            username, _, password = result
        except TypeError:
            return
        return username, password


class Session(
    SessionAuthMixin,
    SessionErrorMixin,
    requests.Session,
):
    """`requests.Session` class with default IGWN authorization handling

    {parameters}

    Examples
    --------
    >>> from igwn_auth_utils.requests import Session
    >>> with Session(token=mytoken) as sess:
    ...     sess.get("https://my.science.stuff/data")
    """


# update the docstrings to include the same parameter info
for _obj in (Session, SessionAuthMixin):
    _obj.__doc__ = _obj.__doc__.format(parameters=_auth_session_parameters)


def get(url, *args, session=None, **kwargs):
    """Request data from a URL via an HTTP ``'GET'`` request

    Parameters
    ----------
    url : `str`,
        the URL to request

    session : `requests.Session`, optional
        the connection session to use, if not given one will be
        created on-the-fly

    *args, **kwargs
        all other keyword arguments are passed directly to
        `requests.Session.get`

    Returns
    -------
    resp : `requets.Response`
        the response object

    See also
    --------
    requests.Session.get
        for information on how the request is performed
    """
    # user's session
    if session:
        return session.get(url, *args, **kwargs)

    # new session
    sess_kwargs = {k: kwargs.pop(k, None) for k in (
        "cert",
        "token",
        "token_audience",
        "token_scope",
    )}
    with Session(url=url, **sess_kwargs) as session:
        return session.get(url, *args, **kwargs)
