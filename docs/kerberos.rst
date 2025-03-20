.. sectionauthor:: Duncan Macleod <duncan.macleod@ligo.org>

.. _igwn-auth-utils-kerberos:

#################################
Working with Kerberos credentials
#################################

The LIGO Scientific Collaboration uses `Kerberos <https://web.mit.edu/kerberos/>`__
as an authentication mechanism, both for direct access to services, and to
negotiate access to :doc:`SciTokens <scitokens>`.

This is particularly useful in support of automated applications, for which a
'robot' Kerberos principal is created, and a secure Kerberos keytab file issued,
which allows automating regular creation of access tokens.


===
API
===

`igwn_auth_utils` provides the following methods for interacting with Kerberos:

.. autosummary::
   :toctree: api

   ~igwn_auth_utils.kinit
