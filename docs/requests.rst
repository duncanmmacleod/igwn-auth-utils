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
    :caption: Make a request with `igwn_auth_utils.Session`.

    from igwn_auth_utils import Session
    with Session() as sess:
        sess.get("https://myservice.example.com/api/important/data")

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

   ~igwn_auth_utils.get
   ~igwn_auth_utils.request
   ~igwn_auth_utils.HTTPSciTokenAuth
   ~igwn_auth_utils.Session
   ~igwn_auth_utils.SessionAuthMixin

=====================
Other request methods
=====================

Only the :func:`~igwn_auth_utils.get` and :func:`~igwn_auth_utils.request`
functions are available from the top-level module interface, however all
HTTP methods are supported via functions in the
:mod:`igwn_auth_utils.requests` module:

.. autosummary::
   :toctree: api
   :nosignatures:

   igwn_auth_utils.requests.delete
   igwn_auth_utils.requests.head
   igwn_auth_utils.requests.patch
   igwn_auth_utils.requests.post
   igwn_auth_utils.requests.put

==========================
Authentication credentials
==========================

By default, ``igwn_auth_utils`` will attempt to find both a
:doc:`SciToken <scitokens>` and an :doc:`X.509 credential <x509>`,
to attach to a request.
If a credential or token is found it will be attached, if one isn't found,
no failures or warnings are emitted.
Requests will then be accepted or rejected by the remote application as
appropriate.

``igwn_auth_utils`` supports two environment variables to explicitly enable
(require) or disable automatic discovery of credentials.

.. list-table:: Environment variable values
    :stub-columns: 1

    * - Enable
      - ``y``, ``yes``, ``true``, ``1``
    * - Disable
      - ``n``, ``no``, ``false``, ``0``

If a variable is set to something 'truthy' (``yes``), and a credential of that
type is not found, an error will be raised before the request is sent.
If a variable is set to something 'falsy' (``no``) no attempt will be made
to discover a credential of that type, and no warnings will be emitted.

.. _igwn-auth-utils-find-scitoken:

---------------------------------
``IGWN_AUTH_UTILS_FIND_SCITOKEN``
---------------------------------

Set the ``IGWN_AUTH_UTILS_FIND_SCITOKEN`` variable to control automatic
discovery of :doc:`SciTokens <scitokens>`.

.. tab-set::

    .. tab-item:: Enable

        .. code-block:: bash
            :caption: Require finding a scitoken (``bash``)

            IGWN_AUTH_UTILS_FIND_SCITOKEN=yes

    .. tab-item:: Disable

        .. code-block:: bash
            :caption: Disable finding a scitoken (``bash``)

            IGWN_AUTH_UTILS_FIND_SCITOKEN=no

.. _igwn-auth-utils-find-x509:

-----------------------------
``IGWN_AUTH_UTILS_FIND_X509``
-----------------------------

Set the ``IGWN_AUTH_UTILS_FIND_X509`` variable to control automatic
discovery of :doc:`X.509 certificates <x509>`.

.. tab-set::

    .. tab-item:: Enable

        .. code-block:: bash
            :caption: Require finding an X.509 credential (``bash``)

            IGWN_AUTH_UTILS_FIND_X509=yes

    .. tab-item:: Disable

        .. code-block:: bash
            :caption: Disable finding an X.509 credential (``bash``)

            IGWN_AUTH_UTILS_FIND_X509=no
