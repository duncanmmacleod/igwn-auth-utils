# Copyright 2021 Cardiff University
# Distributed under the terms of the BSD-3-Clause license

"""Custom exceptions for IGWN Auth Utils."""

__author__ = "Duncan Macleod <duncan.macleod@ligo.org>"


class IgwnAuthError(RuntimeError):
    """Error in discovering/validating an IGWN auth credential."""
