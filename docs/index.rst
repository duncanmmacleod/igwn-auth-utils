=================
`igwn-auth-utils`
=================

Python library functions to simplify using `IGWN <https://www.ligo.org>`__
authorisation credentials.

------------
Installation
------------

``igwn-auth-utils`` can be installed via `Conda <https://conda.io>`:

.. code-block:: shell

   conda install -c conda-forge igwn-auth-utils

or `pip <https://pip.pypa.io>`_:

.. code-block:: shell

   python -m pip install igwn-auth-utils

Documentation
-------------

.. automodapi:: igwn_auth_utils
   :no-main-docstr:
   :no-inheritance-diagram:
   :headings: ^"

.. automodapi:: igwn_auth_utils.requests
   :no-main-docstr:
   :no-inheritance-diagram:
   :headings: ^"
   :skip: netrc
   :skip: urlparse
   :skip: IgwnAuthError
   :skip: find_scitoken
   :skip: find_x509_credentials
   :skip: scitoken_authorization_header

-------
Support
-------

To ask a question, report an issue, or suggest a change, please
`open a ticket on GitHub <https://github.com/duncanmmacleod/igwn-auth-utils/issues/>`_.
