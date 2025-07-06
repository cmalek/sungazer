========
sungazer
========

.. toctree::
   :maxdepth: 2
   :caption: Getting Started
   :hidden:

   overview/installation
   overview/quickstart

.. toctree::
   :maxdepth: 2
   :caption: User Guide
   :hidden:

   overview/connecting
   overview/configuration
   overview/using_client
   overview/using_cli

.. toctree::
   :maxdepth: 2
   :caption: Reference
   :hidden:

   overview/bankruptcy
   overview/sunstrong
   api/models
   api/client

.. toctree::
   :maxdepth: 2
   :caption: Runbook
   :hidden:

   runbook/contributing

Current version is |release|.

``sungazer`` is a Python library that provides can be used to interact with the
SunPower PVS6 API.

Legal
-----

This library is not affiliated with SunPower Corporation or SunStrong.  It is
a community-driven project that provides a way to interact with the SunPower
PVS6 API using Python.

This documentation and software is published solely for the purpose of enabling
interoperability with independently developed monitoring tools, systems, or
components. No original source code or proprietary content is reproduced, and no
attempt has been made to circumvent any access control mechanisms protected
under the DMCA.

This work is intended to support compatibility and repair under the exemptions
granted by:

- 17 U.S. Code § 1201(f) (reverse engineering for interoperability),
- The Library of Congress DMCA Rulemakings, and
- Applicable fair use principles under 17 U.S. Code § 107.


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
using Python, granting access to the data that is available in the API.


Impact on Customers
-------------------

The bankruptcy and subsequent asset sale had several major impacts on SunPower customers:

1. **Monitoring Application Changes**: The original SunPower monitoring iOS and
Android applications were modified to hide most functionality behind
subscription paywalls.

2. **Limited Access**: Many features that were previously free became premium
features, requiring monthly or annual subscriptions.

3. **API Access**: While the underlying PVS6 API remained functional, official
documentation and support for direct API access was discontinued.

4. **Data Ownership**: Customers found themselves with limited access to their
own solar system data through official channels.

5. **Customer Support**: SunStrong only took over the leased SunPower systems,
not the systems bought outright or via third party financing.  SunStrong only
answers support tickets -- calling them says to use the ticket system.
Unfortunately, the ticket system requires a login, which is only available if
you are leasing a SunPower system.  Thus you're out of luck if you bought a
system outright or via third party financing.

Current State of SunPower monitoring
------------------------------------

As of June 2025, with the firmware version "2025.06, Build 61839", the situation
for former SunPower customers is as follows:

- **Official Monitoring**: The iOS/Android app provided by SunStrong is limited to real time data; all other data is hidden behind a subscription paywall, currently $9.99/month or $99.99/year (as of June 2025).
- **API Access**: The API on the PVS6 accessed via the installer LAN1 port remains functional but undocumented
- **Installer website**: The installer website on the PVS6 LAN1 port is up, but shows 403 Forbidden.
- **Customer Support**: Only available via the SunStrong ticket system, which requires a login, which is only available if you are leasing a SunPower system (as of June 2025).

For those of us who bought a system outright or via third party financing, we
are out of luck.  SunStrong does not support us, and at any rate the SunPower/SunStrong
applications were extremely limited in functionality (e.g. no per-panel data, no
no export of data, etc.).  We are left with a system that is not supported by
SunStrong in terms of critical monitoring, and we are left to our own devices.

Commercial Alternatives to SunStrong Monitoring
-----------------------------------------------

If you don't want to muck with building your own monitoring solution, there are
a few commercial alternatives to SunStrong monitoring.  We who support ``sungazer``
are not affiliated with any of these companies, and we are not endorsing them.  We
also have no experience with them, but we list them here for completeness.

All of these solutions seem to require replacing your PVS6 with a new monitoring
device (which has associated costs for the hardware and installation), and using
a different monitoring application.

- `Cape Fear Solar Systems Monitoring <https://capefearsolarsystems.com/monitoring-sunpower-systems-in-2025/>`_
- `Enphase Monitoring <https://enphase.com/homeowners/support/sunpower>`_.  Enphase made the inverters that our SunPower systems use.
- `SunPower Monitoring <https://www.sunpower.com/en-us/products/monitoring>`_


The Future
----------

While SunPower continues to operate under new ownership, the focus has shifted
away from supporting legacy monitoring systems. This has created an opportunity
for open-source solutions that can provide customers with the data access they
need without the limitations and costs of official applications.

Libraries like ``sungazer`` help bridge this gap by providing reliable, documented
access to the PVS6 API, allowing customers to maintain full control over their
solar system data and monitoring capabilities.

References
----------

The following documentation sources are tremendously helpful in understanding
the PVS6 API and how to use it, and were referenced heavily in the development
of this library.  Many thanks to the authors for sharing their knowledge and
experience.

- `Brett Durrett: Getting SunPower PVS6 Administrator Access with No Ethernet Port <https://brett.durrett.net/getting-administrator-access-to-sunpower-pvs6-with-no-ethernet-port/>`_
- `Kiel Koleson: PVS6 notes <https://gist.github.com/koleson/5c719620039e0282976a8263c068e85c>`_
- `Gino Ledesma and John Mu: SunPower PVS5x/PVS6 Notes <https://github.com/ginoledesma/sunpower-pvs-exporter/blob/master/sunpower_pvs_notes.md>`_
- `Scott Gruby: Monitoring a SunPower Solar System <https://blog.gruby.com/2020/04/28/monitoring-a-sunpower-solar-system.html>`_
