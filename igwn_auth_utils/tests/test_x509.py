# -*- coding: utf-8 -*-
# Copyright 2021 Cardiff University
# Distributed under the terms of the BSD-3-Clause license

"""Tests for :mod:`igwn_auth_utils.x509`.
"""

__author__ = "Duncan Macleod <duncan.macleod@ligo.org>"

import os
from datetime import (
    datetime,
    timedelta,
)
from pathlib import Path
from unittest import mock

from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import (
    hashes,
    serialization,
)

import pytest

from .. import x509 as igwn_x509


# -- fixtures ---------------

@pytest.fixture
def x509cert(private_key, public_key):
    name = x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, "test"),
    ])
    now = datetime.utcnow()
    return x509.CertificateBuilder(
        issuer_name=name,
        subject_name=name,
        public_key=public_key,
        serial_number=1000,
        not_valid_before=now,
        not_valid_after=now + timedelta(seconds=86400),
    ).sign(private_key, hashes.SHA256())


def _write_x509(cert, path):
    with open(path, "wb") as file:
        file.write(cert.public_bytes(
            serialization.Encoding.PEM,
        ))


@pytest.fixture
def x509cert_path(x509cert, tmp_path):
    cert_path = tmp_path / "x509.pem"
    _write_x509(x509cert, cert_path)
    return cert_path


# -- tests ------------------

@mock.patch.dict("os.environ")
@mock.patch(
    "os.getlogin" if os.name == "nt" else "os.getuid",
    mock.MagicMock(return_value=123),
)
def test_default_cert_path():
    if os.name == "nt":
        os.environ["SYSTEMROOT"] = r"C:\WINDOWS"
        expected = r"C:\WINDOWS\Temp\x509up_123"
    else:
        expected = r"/tmp/x509up_u123"
    assert igwn_x509._default_cert_path() == Path(expected)


def test_is_valid_cert_path(x509cert_path):
    assert igwn_x509.is_valid_cert_path(x509cert_path)


def test_is_valid_cert_path_false(tmp_path):
    assert not igwn_x509.is_valid_cert_path(tmp_path / "does-not-exist")


@mock.patch.dict("os.environ")
def test_find_credentials_x509userproxy(x509cert_path):
    x509cert_filename = str(x509cert_path)
    os.environ["X509_USER_PROXY"] = x509cert_filename
    assert igwn_x509.find_credentials() == (x509cert_filename,) * 2


@mock.patch.dict("os.environ", clear=True)
def test_find_credentials_x509usercertkey(x509cert_path, public_pem_path):
    x509cert_filename = str(x509cert_path)
    x509key_filename = str(public_pem_path)
    os.environ["X509_USER_CERT"] = x509cert_filename
    os.environ["X509_USER_KEY"] = x509key_filename
    assert igwn_x509.find_credentials() == (
        x509cert_filename,
        x509key_filename,
    )


@mock.patch.dict("os.environ", clear=True)
def test_find_credentials_default(x509cert_path):
    with mock.patch("igwn_auth_utils.x509._default_cert_path") as m:
        m.return_value = x509cert_path
        assert igwn_x509.find_credentials() == (str(x509cert_path),) * 2


@mock.patch.dict("os.environ", clear=True)
def test_find_credentials_error(tmp_path):
    with mock.patch("igwn_auth_utils.x509._default_cert_path") as m:
        m.return_value = tmp_path / "does-not-exist"
        with pytest.raises(RuntimeError) as exc:
            igwn_x509.find_credentials()
        assert str(exc.value).startswith(
            "could not find an RFC-3820 compliant X.509 credential",
        )
