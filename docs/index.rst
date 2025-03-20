#################
`igwn-auth-utils`
#################

Python library functions to simplify using `IGWN <https://www.ligo.org>`__
authorisation credentials.

For more information on the different types of credentials that
IGWN member groups use, see
`The IGWN Computing Guide <https://computing.docs.ligo.org/guide/auth/>`_.

============
Installation
============

``igwn-auth-utils`` can be installed via `Conda <https://conda.io>`:

.. code-block:: shell
    :caption: Installing igwn-auth-utils with Conda.

    conda install -c conda-forge igwn-auth-utils

or `pip <https://pip.pypa.io>`_:

.. code-block:: shell
    :caption: Installing igwn-auth-utils with Pip.

    python -m pip install igwn-auth-utils

Binary packages are also available for various Debian and RHEL
distributions supported by the LIGO Scientific Collaboration's
Computing and Software Working Group, see
`the IGWN Computing Guide <https://computing.docs.ligo.org/guide/software/>`__
for details.

=============
Documentation
=============

.. toctree::
    :maxdepth: 1
    :caption: Using credentials

    HTTP(S) requests <requests>

.. toctree::
    :maxdepth: 1
    :caption: Credential utilities

    Kerberos <kerberos>
    SciTokens <scitokens>
    X.509 <x509>

.. toctree::
    :maxdepth: 1
    :caption: API reference

    api/igwn_auth_utils
    api/igwn_auth_utils.requests
    api/igwn_auth_utils.scitokens
    api/igwn_auth_utils.x509

=======
Support
=======

To ask a question, report an issue, or suggest a change, please
`open a ticket on GitLab <https://git.ligo.org/computing/igwn-auth-utils/-/issues/>`_.
If you are not a member of an IGWN collaboration, you can
`open a ticket via email <contact+computing-igwn-auth-utils-11557-issue-@support.ligo.org>`_.
