# -*- coding: utf-8 -*-
# Copyright 2021 Cardiff University
# Distributed under the terms of the BSD-3-Clause license

import os
from datetime import datetime
from pathlib import Path

from cryptography.x509 import load_pem_x509_certificate


def _default_cert_path(prefix="x509up_"):
    """Returns the temporary path for a user's X509 certificate

    Examples
    --------
    On Windows:

    >>> _default_cert_path()
    'C:\\Users\\user\\AppData\\Local\\Temp\\x509up_user'

    On Unix:

    >>> _default_cert_path()
    '/tmp/x509up_u1000'
    """
    if os.name == "nt":  # Windows
        tmpdir = Path(os.environ["SYSTEMROOT"]) / "Temp"
        user = os.getlogin()
    else:  # Unix
        tmpdir = "/tmp"
        user = "u{}".format(os.getuid())
    return Path(tmpdir) / "{}{}".format(prefix, user)


def is_valid_cert_path(path, timeleft=600):
    """Returns True if a ``path`` contains a valid PEM-format X509 certificate
    """
    try:
        with open(path, "rb") as file:
            cert = load_pem_x509_certificate(file.read())
    except (
        OSError,  # file doesn't exist or isn't readable
        ValueError,  # cannot load PEM certificate
    ):
        return False
    return _timeleft(cert) >= timeleft


def _timeleft(cert):
    """Returns the time remaining (in seconds) for a ``cert``
    """
    return (cert.not_valid_after - datetime.utcnow()).total_seconds()


def find_credentials(timeleft=600):
    """Locate X509 certificate and (optionally) private key files.

    This function checks the following paths in order:

    - ``${X509_USER_PROXY}``
    - ``${X509_USER_CERT}`` and ``${X509_USER_KEY}``
    - ``/tmp/x509up_u${UID}``
    - ``~/.globus/usercert.pem`` and ``~/.globus/userkey.pem``

    Note
    ----
    If the ``X509_USER_{PROXY,CERT,KEY}`` variables are set, their paths
    **are not** validated in any way, but are trusted to point at valid,
    non-expired credentials.
    The default paths in `/tmp` and `~/.globus` **are** validated before
    being returned.

    Parameters
    ----------
    timeleft : `int`
        minimum required time left until expiry (in seconds)
        for a certificate to be considered 'valid'

    Returns
    -------
    cert : `str`
        the path of the certificate file that also contains the
        private key, **OR**

    cert, key : `str`
        the paths of the separate cert and private key files

    Raises
    ------
    RuntimeError
        if not certificate files can be found, or if the files found on
        disk cannot be validtted.

    Examples
    --------
    If no environment variables are set, but a short-lived certificate has
    been generated in the default location:

    >>> find_credentials()
    '/tmp/x509up_u1000'

    If a long-lived (grid) certificate has been downloaded:

    >>> find_credentials()
    ('/home/me/.globus/usercert.pem', '/home/me/.globus/userkey.pem')
    """
    # -- check the environment variables (without validation)

    try:
        return os.environ['X509_USER_PROXY']
    except KeyError:
        try:
            return os.environ['X509_USER_CERT'], os.environ['X509_USER_KEY']
        except KeyError:
            pass

    # -- look up some default paths (with validation)

    # 1: /tmp/x509up_u<uid> (cert = key)
    default = str(_default_cert_path())
    if is_valid_cert_path(default, timeleft):
        return default

    # 2: ~/.globus/user{cert,key}.pem
    try:
        globusdir = Path.home() / ".globus"
    except RuntimeError:  # pragma: no cover
        # no 'home'
        pass
    else:
        cert = str(globusdir / "usercert.pem")
        key = str(globusdir / "userkey.pem")
        if (
            is_valid_cert_path(cert, timeleft)  # validate the cert
            and os.access(key, os.R_OK)  # sanity check the key
        ):
            return cert, key

    raise RuntimeError(
        "could not find an RFC-3820 compliant X.509 credential, "
        "please generate one and try again.",
    )
