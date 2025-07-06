Quickstart Guide
================

This guide will get you up and running with ``sungazer`` quickly, showing both
the Python client and command-line interface.

Prerequisites
-------------

- A SunPower PVS6 device on your network
- Python 3.10+ with ``sungazer`` installed
- Network access to your PVS6 device (see :doc:`/overview/connecting`)

Basic Usage with Python Client
------------------------------

The ``SungazerClient`` provides a simple interface to interact with your PVS6 device.

Starting a Session
~~~~~~~~~~~~~~~~~~

First, create a client and start a session:

.. code-block:: python

    from sungazer import SungazerClient

    # Create client (replace with your device's IP address)
    client = SungazerClient(
        base_url="http://sunpowerconsole.com/cgi-bin",  # Your PVS6 IP
        timeout=30,
        serial="ZT01234567890ABCDEF"  # Your device serial
    )

    # Start a session
    session_info = client.session.start()
    print(f"Session started: {session_info.result}")
    print(f"Device: {session_info.supervisor.MODEL}")
    print(f"Serial: {session_info.supervisor.SERIAL}")

Getting Device Information
~~~~~~~~~~~~~~~~~~~~~~~~~~

List all devices connected to your system:

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

Stopping the Session
~~~~~~~~~~~~~~~~~~~~

Always close your session when done:

.. code-block:: python

    # Stop the session
    stop_result = client.session.stop()
    print(f"Session stopped: {stop_result.result}")

Using Context Manager
~~~~~~~~~~~~~~~~~~~~~

For automatic session management, use the context manager:

.. code-block:: python

    with SungazerClient(
        base_url="http://sunpowerconsole.com/cgi-bin",
        serial="ZT01234567890ABCDEF"
    ) as client:
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

Starting a Session
~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    # Start a session with default settings
    sungazer session start

    # Start with custom device
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
    sungazer firmware check

Configuration
-------------

You can configure ``sungazer`` using configuration files or environment variables.

Configuration File
~~~~~~~~~~~~~~~~~~

Create a configuration file at ``~/.sungazer.conf``:

.. code-block:: ini

    [sungazer]
    base_url = http://sunpowerconsole.com/cgi-bin
    timeout = 30
    serial = ZT01234567890ABCDEF

Environment Variables
~~~~~~~~~~~~~~~~~~~~~

Set environment variables:

.. code-block:: bash

    export SUNGAZER_BASE_URL="http://sunpowerconsole.com/cgi-bin"
    export SUNGAZER_TIMEOUT="30"
    sungazer session start

Next Steps
----------

Now that you have the basics working:

1. **Explore Device Data**: Use ``sungazer device pvs``, ``sungazer device inverters``,
   and other device-specific commands to explore your system data.

2. **Monitor Network**: Use ``sungazer network list`` to monitor connectivity.

3. **Check for Updates**: Regularly run ``sungazer firmware check`` to stay updated.

4. **Automate**: Use the Python client in scripts to automate monitoring and data collection.

5. **Advanced Usage**: See :doc:`/overview/using_client` and :doc:`/overview/using_cli` for more advanced features.


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