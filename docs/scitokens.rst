.. sectionauthor:: Duncan Macleod <duncan.macleod@ligo.org>
.. currentmodule:: igwn_auth_utils

.. _igwn-auth-utils-scitokens:

######################
Working with SciTokens
######################

`SciTokens <https://scitokens.org>`__ are a specific implementation of
`JSON Web Token <https://jwt.io/>`__ that are used by IGWN to authorise
access to resources.

Each SciToken declares a number of *claims* that describe the resources that the
bearer of the token is authorised to access; each service that accepts SciTokens
validates the token (that it was issued by a supported token issuer) and
grants or denies access for that request based entirely on the presented claims.

===
API
===

`igwn_auth_utils` provides the following methods for interacting with SciTokens:

.. autosummary::
   :toctree: api

   ~igwn_auth_utils.find_scitoken
   ~igwn_auth_utils.get_scitoken
   ~igwn_auth_utils.scitoken_authorization_header
