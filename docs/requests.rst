.. sectionauthor:: Duncan Macleod <duncan.macleod@ligo.org>

.. _igwn-auth-utils-requests:

############################################
Making HTTP(S) requests with IGWN Auth Utils
############################################

``igwn_auth_utils`` provides a `requests` interface to support
HTTP/HTTPS requests with the IGWN Auth flow.

===========
Basic usage
===========

To use this interface, open a :class:`~igwn_auth_utils.Session`
and make some requests:

.. code-block:: python

   >>> from igwn_auth_utils import Session
   >>> with Session() as sess:
   ...     sess.get("https://myservice.example.com/api/important/data")

The :class:`igwn_auth_utils.Session` class will automatically discover
available SciTokens and X.509 credentials and will send them with the
request to maximise chances of a successfull authorisation.

See the :class:`igwn_auth_utils.Session` documentation for details on
keywords that enable configuring the discovery of each of the credential
types, including disabling/enabling individual credential types, or
disabling all credentials completely.

===
API
===

.. autosummary::
   :toctree: api
   :nosignatures:

   ~igwn_auth_utils.SessionAuthMixin
   ~igwn_auth_utils.Session
   ~igwn_auth_utils.get
