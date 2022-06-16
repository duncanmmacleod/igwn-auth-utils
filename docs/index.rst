#################
`igwn-auth-utils`
#################

.. toctree::
   :hidden:

   Home <self>

Python library functions to simplify using `IGWN <https://www.ligo.org>`__
authorisation credentials.

For more information on the different types of credentials that
IGWN member groups use, see
`The IGWN Computing Guide <https://computing.docs.ligo.org/auth/>`_.

============
Installation
============

``igwn-auth-utils`` can be installed via `Conda <https://conda.io>`:

.. code-block:: shell

   conda install -c conda-forge igwn-auth-utils

or `pip <https://pip.pypa.io>`_:

.. code-block:: shell

   python -m pip install igwn-auth-utils

=============
Documentation
=============

-------------------
``igwn_auth_utils``
-------------------

The ``igwn_auth_utils`` module provides the following objects:

.. currentmodule:: igwn_auth_utils

.. autosummary::
   :toctree: api
   :caption: igwn_auth_utils
   :nosignatures:

   ~find_scitoken
   find_x509_credentials
   scitoken_authorization_header
   IgwnAuthError

----------------------------
``igwn_auth_utils.requests``
----------------------------

``igwn-auth-utils`` provides an optional `requests` interface in the
``igwn_auth_utils.requests`` module.

.. admonition:: ``igwn_auth_utils.requests`` has extra requirements

    This module requires the following extra packages to be installed:

    - `requests`
    - `safe-netrc`

    These can be installed with `pip` by specifying the `[requests]`
    extra when installing ``igwn-auth-utils``:

    .. code-block:: shell

        python -m pip install igwn-auth-utils[requests]

``igwn_auth_utils.requests`` provides the following classes/functions:

.. currentmodule:: igwn_auth_utils.requests

.. autosummary::
   :toctree: api
   :caption: igwn_auth_utils.requests
   :nosignatures:

   SessionAuthMixin
   Session
   get

=======
Support
=======

To ask a question, report an issue, or suggest a change, please
`open a ticket on GitLab <https://git.ligo.org/computing/igwn-auth-utils/-/issues/>`_.
If you are not a member of an IGWN collaboration, you can
`open a ticket via email <contact+computing-igwn-auth-utils-11557-issue-@support.ligo.org>`_.
