# -*- coding: utf-8 -*-
# Copyright 2021 Cardiff University
# Distributed under the terms of the BSD-3-Clause license

"""Utility functions for discovering valid scitokens
"""

__author__ = "Duncan Macleod <duncan.macleod@ligo.org>"

import os
from pathlib import Path

from .error import IgwnAuthError
from scitokens import (
    Enforcer,
    SciToken,
)

WINDOWS = os.name == "nt"

# -- utilities --------------


def is_valid_token(token, audience, scope, timeleft=600):
    enforcer = Enforcer(token["iss"], audience=audience)

    def _validate_timeleft(value):
        exp = float(value)
        return exp >= enforcer._now + timeleft

    enforcer.add_validator("exp", _validate_timeleft)
    scheme, path = scope.split(":", 1)
    return enforcer.test(token, scheme, path)


# -- I/O --------------------

def deserialize_token(raw, **kwargs):
    """Deserialize a token.

    Parameters
    ----------
    raw : `str`
        the raw serialised token content to deserialise

    **kwargs
        all keyword arguments are passed on to
        :meth:`scitokens.SciToken.deserialize`

    Returns
    -------
    token : `scitokens.SciToken`
        the deserialised token

    See also
    --------
    scitokens.SciToken.deserialize
        for details of the deserialisation, and any valid keyword arguments
    """
    return SciToken.deserialize(raw.strip(), **kwargs)


def load_token_file(path, **kwargs):
    """Load a SciToken from a file path.

    Parameters
    ----------
    path : `str`
        the path to the scitokens file

    **kwargs
        all keyword arguments are passed on to :func:`deserialize_token`

    Returns
    -------
    token : `scitokens.SciToken`
        the deserialised token

    Examples
    --------
    To load a token and validate a specific audience:

    >>> load_token('mytoken', audience="my.service.org")

    See also
    --------
    scitokens.SciToken.deserialize
        for details of the deserialisation, and any valid keyword arguments
    """
    with open(path, "r") as fobj:
        return deserialize_token(fobj.read(), **kwargs)


# -- discovery --------------

def find_token(audience, scope, timeleft=600, skip_errors=False, **kwargs):
    """Find and load a `SciToken` for the given ``audience`` and ``scope``.

    Parameters
    ----------
    audience : `str`
        the required audience (``aud``).

    scope : `str`
        the required scope (``scope``).

    timeleft : `int`
        minimum required time left until expiry (in seconds)
        for a token to be considered 'valid'

    skip_errors : `bool`, optional
        skip over errors encoutered when attempting to deserialise
        discovered tokens; this may be useful to skip over invalid
        or expired tokens that exist, for example.

    **kwargs
        all keyword arguments are passed on to
        :meth:`scitokens.SciToken.deserialize`

    Returns
    -------
    token : `scitokens.SciToken`
        the first token that matches the requirements

    Raises
    ------
    ~igwn_auth_utils.IgwnAuthError
        if no valid token can be found

    See also
    --------
    scitokens.SciToken.deserialize
        for details of the deserialisation, and any valid keyword arguments
    """
    # iterate over all of the tokens we can find for this audience
    for token in _find_tokens(audience=audience, **kwargs):
        # parsing a token yielded an exception, handle it here:
        if isinstance(token, Exception):
            if skip_errors:
                continue
            raise token

        # if this token is valid, stop here and return it
        if is_valid_token(token, audience, scope, timeleft):
            return token

    # if we didn't find any valid tokens:
    raise IgwnAuthError(
        "could not find a valid SciToken, "
        "please verify the audience and scope, "
        "or generate a new token and try again",
    )


def _find_tokens(**deserialize_kwargs):
    """Yield all tokens that we can find

    This function will `yield` exceptions that are raised when
    attempting to parse a token that was actually found, so that
    they can be handled by the caller.
    """
    from scitokens.utils.errors import SciTokensException

    def _token_or_exception(func, *args, **kwargs):
        try:
            return func(*args, **kwargs)
        except SciTokensException as exc:
            return exc

    # read token directly from 'SCITOKEN{_FILE}' variable
    for envvar, loader in (
        ('SCITOKEN', deserialize_token),
        ('SCITOKEN_FILE', load_token_file),
    ):
        if envvar in os.environ:
            yield _token_or_exception(
                loader,
                os.environ[envvar],
                **deserialize_kwargs,
            )

    try:
        yield _token_or_exception(SciToken.discover, **deserialize_kwargs)
    except (
        OSError,  # no token
        AttributeError,  # windows doesn't have geteuid
    ) as exc:
        if isinstance(exc, AttributeError) and not (
            WINDOWS
            and "geteuid" in str(exc)
        ):
            raise
        for tokenfile in _find_condor_creds_token_paths():
            yield _token_or_exception(
                load_token_file,
                tokenfile,
                **deserialize_kwargs,
            )


def _find_condor_creds_token_paths():
    """Find all token files in the condor creds directory
    """
    try:
        _condor_creds_dir = Path(os.environ["_CONDOR_CREDS"])
    except KeyError:
        return
    try:
        for f in _condor_creds_dir.iterdir():
            if f.suffix == ".use":
                yield f
    except FileNotFoundError:   # creds dir doesn't exist
        return


# -- HTTP request helper ----

def token_authorization_header(token, scheme="Bearer"):
    """Format an in-memory token for use in an HTTP Authorization Header.

    Parameters
    ----------
    token : `scitokens.SciToken`
        the token to format

    scheme : `str` optional
        the Authorization scheme to use

    Returns
    -------
    header_str : `str`
        formatted content for an `Authorization` header

    Notes
    -----
    See `RFC-6750 <https://datatracker.ietf.org/doc/html/rfc6750>`__
    for details on the ``Bearer`` Authorization token standard.
    """
    return "{} {}".format(
        scheme,
        token._serialized_token or token.serialize().decode("utf-8"),
    )
