Quickstart Guide
================

This guide will get you up and running with ``sungazer`` quickly, showing both
the Python client and command-line interface.

Prerequisites
-------------

- A SunPower PVS6 device
- Follow the :doc:`/overview/installation` instructions to install ``sungazer``
- Network access to your PVS6 device (see :doc:`/overview/connecting`)
- A CAT5e or CAT6 Ethernet cable to connect your PVS6 device to your computer
- Possibly a USB-A to Ethernet adapter if your PVS6 device doesn't have a LAN1 Ethernet port (see :doc:`/overview/connecting`)

Basic Usage with Python Client
------------------------------

The :py:class:`sungazer.client.SungazerClient` provides a simple interface to
interact with your PVS6 device.  You can find the full API reference in the
:doc:`/api/client` section.  See :doc:`/overview/configuration_client` for
configuration options for the Python client.

Getting info about the PVS6 device itself
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. note::

    ``client.session.start()`` will start a session with the PVS6 device.  This
    seems to be only required to **write** to the PVS6 device, but we don't know
    of any of the endpoints that require a session, so we just use it to get info
    about the PVS6 device itself.

.. code-block:: python

    from sungazer import SungazerClient

    # Create client with the default configuration
    client = SungazerClient()

    # Run the session start command to see info about the PVS6 device
    session_info = client.session.start()
    print(f"Device: {session_info.supervisor.MODEL}")
    print(f"Serial: {session_info.supervisor.SERIAL}")

    client.session.stop()

Getting Device Information
~~~~~~~~~~~~~~~~~~~~~~~~~~

List all devices connected to your system.  Note that you don't need to start a
session to do this.

.. code-block:: python

    # Get device list
    devices = client.device.list()

    print(f"Found {len(devices.devices)} devices:")
    for device in devices.devices:
        print(f"- {device.type}: {device.model} (Serial: {device.serial})")

Checking Network Status
~~~~~~~~~~~~~~~~~~~~~~~

Monitor your device's network connectivity:

.. code-block:: python

    # Get network status
    network = client.network.list()

    print(f"System interface: {network.networkstatus.system.interface}")
    print(f"Internet status: {network.networkstatus.system.internet}")
    print(f"SMS status: {network.networkstatus.system.sms}")

    # List all interfaces
    for interface in network.networkstatus.interfaces:
        print(f"Interface {interface.interface}: {interface.internet}")

Checking Firmware
~~~~~~~~~~~~~~~~~

Check if firmware updates are available:

.. code-block:: python

    # Check firmware status
    firmware = client.firmware.check()

    print(f"Firmware check result: {firmware.result}")
    if firmware.url and firmware.url != "none":
        print(f"Update available: {firmware.url}")

Using Context Manager
~~~~~~~~~~~~~~~~~~~~~

For automatic session management, use the context manager:

.. code-block:: python

    with SungazerClient() as client:
        # Session is automatically started
        devices = client.device.list()
        print(f"Found {len(devices.devices)} devices")
        # Session is automatically stopped when exiting the context

Basic Usage with Command Line
-----------------------------

The ``sungazer`` command-line interface provides easy access to all functionality.

Getting Help
~~~~~~~~~~~~

.. code-block:: bash

    # Show main help
    sungazer --help

    # Show help for specific commands
    sungazer session --help
    sungazer device --help
    sungazer network --help
    sungazer firmware --help
    sungazer grid-profile --help

Starting a Session
~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    # Start a session with default settings
    sungazer session start

    # Start with custom IP (if you've bridged the PVS6 to your local network for
    # example)
    sungazer --base-url http://192.168.1.100/cgi-bin session start

Listing Devices
~~~~~~~~~~~~~~~

.. code-block:: bash

    # List all devices
    sungazer device list

    # List devices in table format
    sungazer --output table device list

Checking Network Status
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    # Get network information
    sungazer network list

    # Get network info in table format
    sungazer --output table network list

Checking Firmware
~~~~~~~~~~~~~~~~~

.. code-block:: bash

    # Check firmware status
    >>> sungazer firmware check
    {
        "url": "none"
    }

Configuration for the Command Line Tool
---------------------------------------

If you are connecting your computer directly to the PVS6, typically the defaults
that ship with ``sungazer`` will work.  If you need to change those defaults,
you can create a configuration file at ``~/.sungazer.conf``:

You can configure ``sungazer`` using configuration files or environment
variables.  See :doc:`/overview/configuration_cli` for more details.

Next Steps
----------

Now that you have the basics working:

1. **Usage**: See :doc:`/overview/using_client` and :doc:`/overview/using_cli` for more advanced features.

2. **Explore Device Data**: Use ``sungazer device pvs``, ``sungazer device inverters``,
   and other device-specific commands to explore your system data.

3. **Monitor Network**: Use ``sungazer network list`` to monitor connectivity.

4. **Check for Updates**: Regularly run ``sungazer firmware check`` to see if you need to update your PVS6 firmware.

5. **Automate**: Use the Python client in scripts to automate monitoring and data collection.



Troubleshooting
---------------

Common Issues
~~~~~~~~~~~~~

**Connection Refused**
    - Check that your PVS6 device is powered on and connected to your computer via Ethernet
    - Verify the IP address is correct (see :doc:`/overview/connecting`)
    - Ensure no firewall is blocking the connection

**SSL Certificate Errors**
    - The library automatically handles SSL certificate issues
    - If problems persist, check your device's SSL configuration

Getting Help
------------

- Check the full documentation for detailed examples
- Review the troubleshooting sections in each guide
- Report issues on the GitHub repository