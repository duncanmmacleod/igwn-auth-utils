# `igwn-auth-utils`

Python library functions to simplify using IGWN authorisation credentials.

<https://igwn-auth-utils.readthedocs.io/>

This project is primarily aimed at discovering X.509 credentials and
SciTokens for use with HTTP(S) requests to IGWN-operated services.

## Release status

[![PyPI version](https://badge.fury.io/py/igwn-auth-utils.svg)](http://badge.fury.io/py/igwn-auth-utils)
[![License](https://img.shields.io/pypi/l/igwn-auth-utils.svg)](https://git.ligo.org/computing/igwn-auth-utils/blob/main/LICENSE)
[![DOI](https://zenodo.org/badge/383081505.svg)](https://zenodo.org/badge/latestdoi/383081505)

## Development status

[![Build status](https://git.ligo.org/computing/igwn-auth-utils/badges/main/pipeline.svg)](https://git.ligo.org/computing/igwn-auth-utils/-/pipelines)
![Code coverage](https://git.ligo.org/computing/igwn-auth-utils/badges/main/coverage.svg)
[![Documentation Status](https://readthedocs.org/projects/igwn-auth-utils/badge/?version=latest)](https://igwn-auth-utils.readthedocs.io/en/latest/?badge=latest)

## Installation

The best way to install the latest release is using
[`conda`](https://conda.io/) with the
[`conda-forge`](https://conda-forge.org) channel enabled:

```bash
conda install -c conda-forge igwn-auth-utils
```

The latest release can also be installed using `pip`:

```bash
python -m pip install igwn-auth-utils
```

## Basic usage

To discover an X.509 user credential (proxy) **location**:

```python
>>> from igwn_auth_utils import find_x509_credentials
>>> print(find_x509_credentials())
('/tmp/x509up_u1000', '/tmp/x509up_u1000')
```

To discover (**and deserialise**) a SciToken for a specific
purpose (`audience` and `scope`):

```python
>>> from igwn_auth_utils import find_scitoken
>>> print(find_scitoken("myservice", "read:/mydata"))
<scitokens.scitokens.SciToken object at 0x7fe99ab792e0>
```
