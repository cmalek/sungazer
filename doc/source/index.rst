========
sungazer
========

.. toctree::
   :caption: Runbook
   :hidden:

   runbook/contributing

.. toctree::
   :caption: Reference
   :hidden:

   api/models
   api/mixins
   api/events

.. include:: _services_index.rst

Current version is |release|.

``sungazer`` is a Python library that provides can be used to interact with the
SunPower PVS6 API.

Why make this library?
----------------------

When SunPower entered Chapter 11 bankruptcy in 2023, they sold their monitoring
tools to SunStrong, once part of the SunPower group. The new company has changed
the already poor SunPower monitoring iOS and Android application such that it
hides most of the functionality behind a subscription paywall, and the
application is now very limited.

Furthermore, the SunPower PVS6 API provides a ton of functionality that is not
available in the SunPower monitoring application, and the API is not documented
anywhere. This library provides a way to interact with the SunPower PVS6 API
using Python, and provides a way to access the data that is available in the API.