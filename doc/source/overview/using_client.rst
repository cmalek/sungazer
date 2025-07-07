Using the Python Client
=======================

The ``SungazerClient`` provides a comprehensive Python API for interacting with
SunPower PVS6 devices. This guide covers all available functionality and best practices.

Client Initialization
---------------------

Basic Client Setup
~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from sungazer import SungazerClient

    # Basic initialization
    client = SungazerClient(
        base_url="http://sunpowerconsole.com/cgi-bin",
        timeout=30,
        serial="ZT01234567890ABCDEF"
    )

Advanced Configuration
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # With custom configuration
    client = SungazerClient(
        base_url="https://my-pvs6.local/cgi-bin",  # Custom URL
        timeout=60,  # Longer timeout for slow networks
        serial="ZT01234567890ABCDEF"  # Device serial number
    )

Context Manager Usage
~~~~~~~~~~~~~~~~~~~~~

For automatic session management:

.. code-block:: python

    with SungazerClient(
        base_url="http://sunpowerconsole.com/cgi-bin",
        serial="ZT01234567890ABCDEF"
    ) as client:
        # Session automatically started
        devices = client.device.list()
        # Session automatically stopped when exiting context

Session Management
------------------

The PVS6 API requires an active session for most operations.

Starting a Session
~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Start a new session
    session_info = client.session.start()

    print(f"Session result: {session_info.result}")
    print(f"Device model: {session_info.supervisor.MODEL}")
    print(f"Device serial: {session_info.supervisor.SERIAL}")
    print(f"Software version: {session_info.supervisor.SWVER}")
    print(f"Firmware version: {session_info.supervisor.FWVER}")

Stopping a Session
~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Stop the current session
    stop_result = client.session.stop()
    print(f"Session stopped: {stop_result.result}")

Supervisor Information
~~~~~~~~~~~~~~~~~~~~~~

The session response includes detailed device information:

.. code-block:: python

    session = client.session.start()

    # Access supervisor information
    supervisor = session.supervisor
    print(f"Model: {supervisor.MODEL}")
    print(f"Serial: {supervisor.SERIAL}")
    print(f"Software Version: {supervisor.SWVER}")
    print(f"Firmware Version: {supervisor.FWVER}")
    print(f"Build Number: {supervisor.BUILD}")
    print(f"EASIC Version: {supervisor.EASICVER}")
    print(f"SC Version: {supervisor.SCVER}")
    print(f"SC Build: {supervisor.SCBUILD}")
    print(f"WN Model: {supervisor.WNMODEL}")
    print(f"WN Version: {supervisor.WNVER}")
    print(f"WN Serial: {supervisor.WNSERIAL}")

Device Management
-----------------

The device client provides access to all connected devices in your solar system.

Listing All Devices
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Get list of all devices
    devices = client.device.list()

    print(f"Total devices found: {len(devices.devices)}")

    for device in devices.devices:
        print(f"Type: {device.type}")
        print(f"Model: {device.model}")
        print(f"Serial: {device.serial}")
        print(f"Status: {device.status}")
        print("---")

Device-Specific Data
~~~~~~~~~~~~~~~~~~~~

Access specific device types:

.. code-block:: python

    devices = client.device.list()

    # Get PV (solar panel) devices
    pvs_devices = devices.pvs
    print(f"PV devices: {len(pvs_devices)}")

    # Get inverter devices
    inverters = devices.inverters
    print(f"Inverters: {len(inverters)}")

    # Get production meter
    production_meter = devices.production_meter
    if production_meter:
        print(f"Production meter: {production_meter.model}")

    # Get consumption meter
    consumption_meter = devices.consumption_meter
    if consumption_meter:
        print(f"Consumption meter: {consumption_meter.model}")

Device Details
~~~~~~~~~~~~~~

Get detailed information about specific device types:

.. code-block:: python

    devices = client.device.list()

    # PV device details
    if devices.pvs:
        pv = devices.pvs[0]
        print(f"PV Device: {pv.model}")
        print(f"Serial: {pv.serial}")
        print(f"Status: {pv.status}")

    # Inverter details
    if devices.inverters:
        for inv in devices.inverters:
            print(f"Inverter: {inv.model}")
            print(f"Serial: {inv.serial}")
            print(f"Status: {inv.status}")

Network Management
------------------

Monitor and manage network connectivity.

Network Status Overview
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Get overall network status
    network = client.network.list()

    # System-level information
    system = network.networkstatus.system
    print(f"Primary interface: {system.interface}")
    print(f"Internet status: {system.internet}")
    print(f"SMS status: {system.sms}")

    # Timestamp
    print(f"Last updated: {network.networkstatus.ts}")

Interface Details
~~~~~~~~~~~~~~~~~

Examine individual network interfaces:

.. code-block:: python

    network = client.network.list()

    for interface in network.networkstatus.interfaces:
        print(f"\nInterface: {interface.interface}")
        print(f"  Internet: {interface.internet}")
        print(f"  State: {interface.state}")
        print(f"  Link: {interface.link}")

        if interface.ipaddr:
            print(f"  IP Address: {interface.ipaddr}")

        # WiFi-specific information
        if interface.ssid:
            print(f"  SSID: {interface.ssid}")
            print(f"  Status: {interface.status}")

        # Cellular-specific information
        if interface.provider:
            print(f"  Provider: {interface.provider}")
            print(f"  SIM Status: {interface.sim}")
            print(f"  Modem Status: {interface.modem}")
            print(f"  Primary: {interface.is_primary}")
            print(f"  Always On: {interface.is_always_on}")

Firmware Management
-------------------

Check and manage firmware updates.

Firmware Status
~~~~~~~~~~~~~~~

.. note::

    Even though the PVS6 API has an endpoint to check for firmware updates, I'm
    not sure now with the new OTA (over-the-air) firmware updates in firmwares
    2025.05 and later that SunStrong has pushed out that this is still useful.

.. code-block:: python

    # Check firmware status
    firmware = client.firmware.check()

    if firmware.url and firmware.url is not None:
        print(f"Update available: {firmware.url}")
    else:
        print("No firmware update available")

Grid Profile Management
-----------------------

Manage or view the grid profile settings for your solar system.

A grid profile is a collection of utility-approved operating parameters for a
system. Selecting the appropriate grid profile ensures compliance and
interoperability with the local electric utility.

Get Current Profile
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Get current grid profile information
    profile = client.grid_profile.get()

    print(f"Result: {profile.result}")
    print(f"Active profile: {profile.active_name}")
    print(f"Active ID: {profile.active_id}")
    print(f"Pending profile: {profile.pending_name}")
    print(f"Pending ID: {profile.pending_id}")
    print(f"Support: {profile.percent}%")
    print(f"Supported by: {profile.supported_by}")
    print(f"Status: {profile.status}")

Refresh Grid Profile
~~~~~~~~~~~~~~~~~~~~

.. important::

    I suspect that this causes internal state of the PVS6 to be updated, so use
    this with caution.

.. code-block:: python

    # Refresh grid profile
    refresh_result = client.grid_profile.refresh()

    print(f"Refresh result: {refresh_result.result}")
    print(f"Active profile: {refresh_result.active_name}")
    print(f"Active ID: {refresh_result.active_id}")
    print(f"Pending profile: {refresh_result.pending_name}")
    print(f"Pending ID: {refresh_result.pending_id}")
    print(f"Progress: {refresh_result.percent}%")
    print(f"Supported by: {refresh_result.supported_by}")
    print(f"Status: {refresh_result.status}")

Error Handling
--------------

Proper error handling is essential for robust applications.

HTTP Errors
~~~~~~~~~~~

.. code-block:: python

    try:
        devices = client.device.list()
    except httpx.HTTPStatusError as e:
        print(f"HTTP error: {e.response.status_code}")
        print(f"Error details: {e.response.text}")
    except httpx.ConnectError as e:
        print(f"Connection error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

Session Errors
~~~~~~~~~~~~~~

.. code-block:: python

    try:
        session = client.session.start()
    except ValueError as e:
        print(f"Session error: {e}")
        # Session errors often indicate device issues
    except Exception as e:
        print(f"Unexpected error: {e}")

Best Practices
--------------

Error Recovery
~~~~~~~~~~~~~~

Implement retry logic for network operations:

.. code-block:: python

    import time
    from httpx import HTTPStatusError

    def get_devices_with_retry(client, max_retries=3):
        for attempt in range(max_retries):
            try:
                return client.device.list()
            except HTTPStatusError as e:
                if e.response.status_code == 500 and attempt < max_retries - 1:
                    print(f"Attempt {attempt + 1} failed, retrying...")
                    time.sleep(2 ** attempt)  # Exponential backoff
                    continue
                raise
        return None

Resource Management
~~~~~~~~~~~~~~~~~~~

Always close clients when done:

.. code-block:: python

    client = SungazerClient()
    try:
        # Use the client
        devices = client.device.list()
    finally:
        client.close()  # Always close

Performance Considerations
--------------------------

Connection Reuse
~~~~~~~~~~~~~~~~

The client reuses HTTP connections for efficiency:

.. code-block:: python

    # Multiple operations use the same connection
    with SungazerClient() as client:
        session = client.session.start()
        devices = client.device.list()
        network = client.network.list()
        firmware = client.firmware.check()
        # All operations use the same HTTP connection

Timeout Configuration
~~~~~~~~~~~~~~~~~~~~~

Adjust timeouts based on your network:

.. code-block:: python

    # For slow networks
    client = SungazerClient(
        base_url="http://sunpowerconsole.com/cgi-bin",
        timeout=60  # Longer timeout
    )

    # For fast local networks
    client = SungazerClient(
        base_url="http://sunpowerconsole.com/cgi-bin",
        timeout=10  # Shorter timeout
    )

Advanced Usage
--------------

Custom HTTP Client
~~~~~~~~~~~~~~~~~~

For advanced HTTP configuration:

.. code-block:: python

    import httpx

    # Create custom HTTP client
    http_client = httpx.Client(
        timeout=httpx.Timeout(30.0),
        headers={"User-Agent": "Sungazer/1.0"},
        verify=False  # Disable SSL verification if needed
    )

    # Use with SungazerClient
    client = SungazerClient(
        base_url="http://sunpowerconsole.com/cgi-bin",
        client=http_client
    )

Data Processing
~~~~~~~~~~~~~~~

Process device data for analysis:

.. code-block:: python

    def analyze_system_health(client):
        """Analyze overall system health."""
        devices = client.device.list()
        network = client.network.list()

        # Check device status
        device_status = {
            device.type: device.status
            for device in devices.devices
        }

        # Check network status
        network_status = {
            interface.interface: interface.internet
            for interface in network.networkstatus.interfaces
        }

        return {
            "devices": device_status,
            "network": network_status,
            "timestamp": network.networkstatus.ts
        }

Automation Examples
-------------------

Monitoring Script
~~~~~~~~~~~~~~~~~

.. code-block:: python

    import time
    from datetime import datetime

    def monitor_system():
        client = SungazerClient(base_url="http://192.168.1.100/cgi-bin")

        try:
            while True:
                try:
                    devices = client.device.list()
                    network = client.network.list()

                    print(f"[{datetime.now()}] System Status:")
                    print(f"  Devices: {len(devices.devices)}")
                    print(f"  Internet: {network.networkstatus.system.internet}")

                    time.sleep(300)  # Check every 5 minutes

                except Exception as e:
                    print(f"Error during monitoring: {e}")
                    time.sleep(60)  # Wait before retry

        finally:
            client.close()

Data Collection
~~~~~~~~~~~~~~~

.. code-block:: python

    import json
    from datetime import datetime

    def collect_system_data():
        with SungazerClient() as client:
            data = {
                "timestamp": datetime.now().isoformat(),
                "devices": client.device.list().model_dump(),
                "network": client.network.list().model_dump(),
                "firmware": client.firmware.check().model_dump()
            }

            # Save to file
            with open(f"system_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", "w") as f:
                json.dump(data, f, indent=2, default=str)

            return data