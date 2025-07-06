Client API Reference
====================

This page documents the Python client API for interacting with SunPower PVS6 devices.

SungazerClient
--------------

The main client class for interacting with PVS6 devices.

.. autoclass:: sungazer.client.SungazerClient
   :members:
   :show-inheritance:
   :inherited-members:

BaseClient
----------

Base client with common HTTP methods.

.. autoclass:: sungazer.client.BaseClient
   :members:
   :show-inheritance:
   :inherited-members:

SessionClient
-------------

Client for session operations.

.. autoclass:: sungazer.client.SessionClient
   :members:
   :show-inheritance:
   :inherited-members:

NetworkClient
-------------

Client for network operations.

.. autoclass:: sungazer.client.NetworkClient
   :members:
   :show-inheritance:
   :inherited-members:

DeviceClient
------------

Client for device operations.

.. autoclass:: sungazer.client.DeviceClient
   :members:
   :show-inheritance:
   :inherited-members:

FirmwareClient
--------------

Client for firmware operations.

.. autoclass:: sungazer.client.FirmwareClient
   :members:
   :show-inheritance:
   :inherited-members:

GridProfileClient
-----------------

Client for grid profile operations.

.. autoclass:: sungazer.client.GridProfileClient
   :members:
   :show-inheritance:
   :inherited-members:

Usage Examples
--------------

Basic Client Usage
~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from sungazer import SungazerClient

    # Create client
    client = SungazerClient(
        base_url="http://sunpowerconsole.com/cgi-bin",
        timeout=30,
        serial="ZT01234567890ABCDEF"
    )

    # Start session
    session = client.session.start()
    print(f"Session started: {session.result}")

    # Get devices
    devices = client.device.list()
    print(f"Found {len(devices.devices)} devices")

    # Get network status
    network = client.network.list()
    print(f"Internet status: {network.networkstatus.system.internet}")

    # Stop session
    client.session.stop()

Context Manager Usage
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    with SungazerClient(
        base_url="http://sunpowerconsole.com/cgi-bin",
        serial="ZT01234567890ABCDEF"
    ) as client:
        # Session automatically started
        devices = client.device.list()
        network = client.network.list()
        firmware = client.firmware.check()
        # Session automatically stopped

Session Management
~~~~~~~~~~~~~~~~~~

.. code-block:: python

    client = SungazerClient(base_url="http://sunpowerconsole.com/cgi-bin")

    # Start session
    session = client.session.start()
    print(f"Device: {session.supervisor.MODEL}")
    print(f"Serial: {session.supervisor.SERIAL}")
    print(f"Version: {session.supervisor.SWVER}")

    # Stop session
    stop_result = client.session.stop()
    print(f"Session stopped: {stop_result.result}")

Device Operations
~~~~~~~~~~~~~~~~~

.. code-block:: python

    client = SungazerClient(base_url="http://sunpowerconsole.com/cgi-bin", serial="ZT01234567890ABCDEF")

    # Get info about the PVS6 itself
    client.session.start()

    # Get all devices
    devices = client.device.list()

    # Access specific device types
    pvs_devices = devices.pvs
    inverters = devices.inverters
    production_meter = devices.production_meter
    consumption_meter = devices.consumption_meter

    client.session.stop()

Network Operations
~~~~~~~~~~~~~~~~~~

.. code-block:: python

    client = SungazerClient(base_url="http://sunpowerconsole.com/cgi-bin", serial="ZT01234567890ABCDEF")
    client.session.start()

    # Get network status
    network = client.network.list()

    # System information
    system = network.networkstatus.system
    print(f"Primary interface: {system.interface}")
    print(f"Internet: {system.internet}")
    print(f"SMS: {system.sms}")

    # Interface details
    for interface in network.networkstatus.interfaces:
        print(f"Interface {interface.interface}: {interface.internet}")

    client.session.stop()

Firmware Operations
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    client = SungazerClient(base_url="http://sunpowerconsole.com/cgi-bin")
    client.session.start()

    # Check firmware
    firmware = client.firmware.check()
    print(f"Current version: {firmware.version}")

    if firmware.url and firmware.url != "none":
        print(f"Update available: {firmware.url}")
    else:
        print("No update available")

    client.session.stop()

Grid Profile Operations
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    client = SungazerClient(base_url="http://sunpowerconsole.com/cgi-bin")
    client.session.start()

    # Get current profile
    profile = client.grid_profile.get()
    print(f"Active profile: {profile.active_name}")
    print(f"Status: {profile.status}")

    # Refresh profile
    refresh = client.grid_profile.refresh()
    print(f"Refresh result: {refresh.result}")

    client.session.stop()

Error Handling
--------------

HTTP Errors
~~~~~~~~~~~

.. code-block:: python

    import httpx
    from sungazer import SungazerClient

    client = SungazerClient(base_url="http://sunpowerconsole.com/cgi-bin")

    try:
        session = client.session.start()
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

    from sungazer import SungazerClient

    client = SungazerClient(base_url="http://sunpowerconsole.com/cgi-bin")

    try:
        session = client.session.start()
    except ValueError as e:
        print(f"Session error: {e}")
        # Session errors often indicate device issues
    except Exception as e:
        print(f"Unexpected error: {e}")

Advanced Usage
--------------

Custom HTTP Client
~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import httpx
    from sungazer import SungazerClient

    # Create custom HTTP client
    http_client = httpx.Client(
        timeout=httpx.Timeout(60.0),
        headers={"User-Agent": "Sungazer/1.0"},
        verify=False  # Disable SSL verification
    )

    # Use custom client
    client = SungazerClient(
        base_url="http://sunpowerconsole.com/cgi-bin",
        client=http_client
    )

    with client:
        devices = client.device.list()

Retry Logic
~~~~~~~~~~~

.. code-block:: python

    import time
    from httpx import HTTPStatusError
    from sungazer import SungazerClient

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

    client = SungazerClient(base_url="http://sunpowerconsole.com/cgi-bin")
    with client:
        devices = get_devices_with_retry(client)

Data Processing
~~~~~~~~~~~~~~~

.. code-block:: python

    from sungazer import SungazerClient

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

    client = SungazerClient(base_url="http://sunpowerconsole.com/cgi-bin")
    with client:
        health = analyze_system_health(client)
        print(f"System health: {health}")

Monitoring Script
~~~~~~~~~~~~~~~~~

.. code-block:: python

    import time
    from datetime import datetime
    from sungazer import SungazerClient

    def monitor_system():
        client = SungazerClient(base_url="http://sunpowerconsole.com/cgi-bin")

        try:
            client.session.start()

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
            client.session.stop()
            client.close()

Data Collection
~~~~~~~~~~~~~~~

.. code-block:: python

    import json
    from datetime import datetime
    from sungazer import SungazerClient

    def collect_system_data():
        with SungazerClient(base_url="http://sunpowerconsole.com/cgi-bin") as client:
            data = {
                "timestamp": datetime.now().isoformat(),
                "devices": client.device.list().model_dump(),
                "network": client.network.list().model_dump(),
                "firmware": client.firmware.check().model_dump()
            }

            # Save to file
            filename = f"system_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, "w") as f:
                json.dump(data, f, indent=2, default=str)

            return data

Best Practices
--------------

Session Management
~~~~~~~~~~~~~~~~~~

Always manage sessions properly:

.. code-block:: python

    # Good: Use context manager
    with SungazerClient(base_url="http://sunpowerconsole.com/cgi-bin") as client:
        devices = client.device.list()
        # Session automatically managed

    # Good: Explicit session management
    client = SungazerClient(base_url="http://sunpowerconsole.com/cgi-bin")
    try:
        client.session.start()
        devices = client.device.list()
    finally:
        client.session.stop()
        client.close()

Resource Management
~~~~~~~~~~~~~~~~~~~

Always close clients when done:

.. code-block:: python

    client = SungazerClient(base_url="http://sunpowerconsole.com/cgi-bin")
    try:
        # Use the client
        devices = client.device.list()
    finally:
        client.close()  # Always close

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

Performance Considerations
--------------------------

Connection Reuse
~~~~~~~~~~~~~~~~

The client reuses HTTP connections for efficiency:

.. code-block:: python

    # Multiple operations use the same connection
    with SungazerClient(base_url="http://sunpowerconsole.com/cgi-bin") as client:
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

SSL Configuration
~~~~~~~~~~~~~~~~~

Handle SSL certificate issues:

.. code-block:: python

    import httpx
    from sungazer import SungazerClient

    # Create client with SSL verification disabled
    http_client = httpx.Client(verify=False)

    client = SungazerClient(
        base_url="https://sunpowerconsole.com/cgi-bin",
        client=http_client
    )

API Reference Details
---------------------

Method Parameters
~~~~~~~~~~~~~~~~~

All client methods accept standard parameters:

- **base_url**: The base URL for API requests
- **timeout**: Request timeout in seconds
- **serial**: Device serial number (optional)

Return Types
~~~~~~~~~~~~

All methods return Pydantic models:

- **SessionClient.start()**: Returns ``StartResponse``
- **SessionClient.stop()**: Returns ``StopResponse``
- **NetworkClient.list()**: Returns ``GetCommResponse``
- **DeviceClient.list()**: Returns ``DeviceDetailResponse``
- **FirmwareClient.check()**: Returns ``CheckFWResponse``
- **GridProfileClient.get()**: Returns ``GridProfileGetResponse``
- **GridProfileClient.refresh()**: Returns ``GridProfileRefreshResponse``

Error Types
~~~~~~~~~~~

Common error types:

- **httpx.HTTPStatusError**: HTTP status errors (4xx, 5xx)
- **httpx.ConnectError**: Connection errors
- **ValueError**: Session and validation errors
- **Exception**: Other unexpected errors