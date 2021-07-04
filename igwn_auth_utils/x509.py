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
    """Locate X509 certificate and key files.

    This function checks the following paths in order:

    - ``${X509_USER_PROXY}``
    - ``${X509_USER_CERT}`` and ``${X509_USER_KEY}``
    - ``/tmp/x509up_u${UID}``

    Parameters
    ----------
    timeleft : `int`
        minimum required time left until expiry (in seconds)
        for a certificate to be considered 'valid'

    Returns
    -------
    cert : `str`
        the path of the certificate file

    key : `str`
        the path of the key file (this may be the same as ``cert``)

    Raises
    ------
    RuntimeError
        if not certificate files can be found, or if the files found on
        disk cannot be validtted.
    """
    try:  # use X509_USER_PROXY from environment if set
        cert = key = os.environ['X509_USER_PROXY']
    except KeyError:
        try:  # otherwise use _CERT and _KEY from env
            cert = os.environ['X509_USER_CERT']
            key = os.environ['X509_USER_KEY']
        except KeyError:  # otherwise fall back to default path
            cert = key = _default_cert_path("x509up_")

    if (
        is_valid_cert_path(cert, timeleft)  # validate the cert properly
        and os.access(key, os.R_OK)  # sanity check the key
    ):
        return str(cert), str(key)

    raise RuntimeError(
        "could not find an RFC-3820 compliant X.509 credential, "
        "please generate one and try again.",
    )
