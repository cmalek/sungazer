Using the Command Line Interface
================================

The ``sungazer`` command-line interface provides easy access to all PVS6 functionality
from the terminal. This guide covers all available commands and options.

Getting Help
------------

Basic Help
~~~~~~~~~~

.. code-block:: bash

    # Show main help
    sungazer --help

    # Show help for specific command groups
    sungazer session --help
    sungazer device --help
    sungazer network --help
    sungazer firmware --help
    sungazer grid-profile --help

Command Structure
-----------------

The CLI follows a hierarchical command structure:

.. code-block:: bash

    sungazer [global-options] <command-group> <subcommand> [options]

Global Options
--------------

Common options available for all commands:

.. code-block:: bash

    # Specify custom base URL
    sungazer --base-url http://192.168.1.100/cgi-bin session start

    # Set custom timeout
    sungazer --timeout 60 device list

    # Choose output format
    sungazer --output table network list

    # Use environment variables to change configuration
    export SUNGAZER_BASE_URL="http://192.168.1.100/cgi-bin"
    export SUNGAZER_TIMEOUT="30"
    sungazer session start

Session Management
------------------

Session commands manage the connection to your PVS6 device.

Starting a Session
~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    # Start a new session
    sungazer session start

    # Start with custom device
    sungazer --base-url http://sunpowerconsole.com/cgi-bin session start

    # Start with verbose output
    sungazer --output table session start

Example output:

.. code-block:: json

    {
      "result": "succeed",
      "supervisor": {
        "MODEL": "PVS6",
        "SERIAL": "ZT01234567890ABCDEF",
        "SWVER": "2021.9, Build 41001",
        "FWVER": "1.0.0",
        "BUILD": 41001,
        "EASICVER": 131329,
        "SCVER": 16504,
        "SCBUILD": 1185,
        "WNMODEL": 400,
        "WNVER": 3000,
        "WNSERIAL": 16
      }
    }

Stopping a Session
~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    # Stop the current session
    sungazer session stop

    # Stop with custom output format
    sungazer --output table session stop

Device Management
-----------------

Device commands provide access to all connected devices in your solar system.

Listing All Devices
~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    # List all devices
    sungazer device list

    # List in table format
    sungazer --output table device list

Example JSON output:

.. code-block:: json

{
	"devices":	[{
			"DETAIL":	"detail",
			"STATE":	"working",
			"STATEDESCR":	"Working",
			"SERIAL":	"ZT21234123451234123",
			"MODEL":	"PV Supervisor PVS6",
			"HWVER":	"6.02",
			"SWVER":	"2025.06, Build 61839",
			"DEVICE_TYPE":	"PVS",
			"DATATIME":	"2025,06,21,23,24,05",
			"dl_err_count":	"0",
			"dl_comm_err":	"2573",
			"dl_skipped_scans":	"0",
			"dl_scan_time":	"14",
			"dl_untransmitted":	"0",
			"dl_uptime":	"8003",
			"dl_cpu_load":	"0.46",
			"dl_mem_used":	"78348",
			"dl_flash_avail":	"59052",
			"panid":	590287501,
			"CURTIME":	"2025,06,22,00,16,18"
		}, {
			"ISDETAIL":	true,
			"SERIAL":	"PVS6M12341231p",
			"TYPE":	"PVS5-METER-P",
			"STATE":	"working",
			"STATEDESCR":	"Working",
			"MODEL":	"PVS6M0400p",
			"DESCR":	"Power Meter PVS6M12341231p",
			"DEVICE_TYPE":	"Power Meter",
			"interface":	"mime",
			"production_subtype_enum":	"GROSS_PRODUCTION_SITE",
			"subtype":	"GROSS_PRODUCTION_SITE",
			"SWVER":	"3000",
			"PORT":	"",
			"DATATIME":	"2025,06,22,00,16,18",
			"ct_scl_fctr":	"50",
			"net_ltea_3phsum_kwh":	"20733.1699",
			"p_3phsum_kw":	"0.5154",
			"q_3phsum_kvar":	"-0.0126",
			"s_3phsum_kva":	"0.5209",
			"tot_pf_rto":	"0.9962",
			"freq_hz":	"60",
			"i_a":	"2.1162",
			"v12_v":	"246.1551",
			"CAL0":	"50",
			"origin":	"data_logger",
			"OPERATION":	"noop",
			"CURTIME":	"2025,06,22,00,16,19"
		},
        ...
    ]
}

Device-Specific Commands
~~~~~~~~~~~~~~~~~~~~~~~~

Access specific device types:

.. code-block:: bash

    # Get PV (solar panel) devices
    sungazer device pvs

    # Get inverter devices (your actual per-solar panel outputs)
    sungazer device inverters

    # Get production meter (how much electricity you're producing)
    sungazer device production-meter

    # Get consumption meter (how much electricity you're using)
    sungazer device consumption-meter

    # All commands support table output
    sungazer --output table device pvs

Network Management
------------------

Network commands monitor and manage network connectivity.

Network Status
~~~~~~~~~~~~~~

.. code-block:: bash

    # Get network status
    sungazer network list

    # Get network status in table format
    sungazer --output table network list

Example JSON output:

.. code-block:: json

    {
      "result": "succeed",
      "networkstatus": {
        "interfaces": [
          {
            "interface": "wan",
            "internet": "down",
            "ipaddr": "",
            "link": "disconnected",
            "mode": "wan",
            "sms": "unreachable",
            "state": "down"
          },
          {
            "interface": "sta0",
            "internet": "up",
            "ipaddr": "192.168.10.239",
            "ssid": "Starfield",
            "status": "connected",
            "sms": "reachable"
          }
          ...
        ],
        "system": {
          "interface": "sta0",
          "internet": "up",
          "sms": "reachable"
        },
        "ts": "1635315583"
      }
    }

Firmware Management
-------------------

Firmware commands check and manage firmware updates.

Check Firmware
~~~~~~~~~~~~~~

.. code-block:: bash

    # Check firmware status
    sungazer firmware check

    # Check firmware with table output
    sungazer --output table firmware check

Example output:

.. code-block:: json

    {
      "url": "none",
    }

Grid Profile Management
-----------------------

Grid profile commands manage grid profile settings.

A grid profile is a collection of utility-approved operating parameters for a
system. Selecting the appropriate grid profile ensures compliance and
interoperability with the local electric utility.

Get Current Profile
~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    # Get current grid profile
    sungazer grid-profile get

    # Get profile in table format
    sungazer --output table grid-profile get

Example output:

.. code-block:: json

    {
      "result": "succeed",
      "active_name": "IEEE-1547a-2014 + 2020 CA Rule21",
      "active_id": "816bf3302d337a42680b996227ddbc46abf9cd05",
      "pending_name": "IEEE-1547a-2014 + 2020 CA Rule21",
      "pending_id": "816bf3302d337a42680b996227ddbc46abf9cd05",
      "percent": 100,
      "supported_by": "ALL",
      "status": "success"
    }

Refresh Grid Profile
~~~~~~~~~~~~~~~~~~~~

.. important::

    I suspect that this causes internal state of the PVS6 to be updated, so use
    this with caution.

.. code-block:: bash

    # Refresh grid profile
    sungazer grid-profile refresh

    # Refresh with table output
    sungazer --output table grid-profile refresh

Output Formats
--------------

JSON Format (Default)
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    # Default JSON output
    sungazer device list

    # Pretty-printed JSON
    sungazer --output json device list

Table Format
~~~~~~~~~~~~

.. code-block:: bash

    # Table output for better readability
    sungazer --output table device list

    # Table output for network status
    sungazer --output table network list

Configuration
-------------

See :doc:`/overview/configuration` for details on how to configure ``sungazer``
for your specific PVS6 monitoring use case.

Examples
--------

Basic Usage Examples
~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    # Start session and check devices
    sungazer session start
    sungazer device list

    # Check network status
    sungazer network list

    # Check firmware
    sungazer firmware check

    # Stop session
    sungazer session stop

Advanced Usage Examples
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    # Monitor system health
    sungazer --output table session start
    sungazer --output table device list
    sungazer --output table network list
    sungazer --output table firmware check
    sungazer session stop

    # Use with custom hostname or IP address
    sungazer --base-url http://192.168.1.100/cgi-bin \
             --output table \
             session start

    # Check specific device types
    sungazer device pvs
    sungazer device inverters
    sungazer device production-meter
    sungazer device consumption-meter

Scripting Examples
~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    #!/bin/bash
    # Monitor script example

    echo "Starting system monitoring..."

    # Start session
    sungazer session start

    # Check devices
    echo "Device Status:"
    sungazer --output table device list

    # Check network
    echo "Network Status:"
    sungazer --output table network list

    # Check firmware
    echo "Firmware Status:"
    sungazer --output table firmware check

    # Stop session
    sungazer session stop

    echo "Monitoring complete."

Error Handling
--------------

Common Error Scenarios
~~~~~~~~~~~~~~~~~~~~~~

**Connection Refused**
    .. code-block:: bash

        # Error: Connection refused
        sungazer session start
        # Error: Failed to connect to http://sunpowerconsole.com/cgi-bin

        # Solution: Check device IP and connectivity
        telnet sunpowerconsole.com 443

**Session Errors**
    .. code-block:: bash

        # Error: Session failed
        sungazer session start
        # Error: Start failed: 500 Internal Server Error

        # Solution: Check device status and restart if needed

**Timeout Errors**
    .. code-block:: bash

        # Error: Request timeout
        sungazer device list
        # Error: Request timed out

        # Solution: Increase timeout
        sungazer --timeout 60 device list

**SSL Certificate Errors**
    .. code-block:: bash

        # Error: SSL certificate verification failed
        sungazer session start

        # Solution: The library automatically handles SSL issues
        # If problems persist, open an issue on the GitHub repository

Troubleshooting
---------------

Debugging Commands
~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    # Check if device is reachable
    telnet sunpowerconsole.com 443

    # Test basic connectivity
    curl --no-check-certificate -v http://sunpowerconsole.com/cgi-bin/dl_cgi?Command=Start

    # Test with verbose output
    sungazer --output table session start

Common Issues
~~~~~~~~~~~~~

**Device Not Found**
    - Verify the IP address or hostname of the PVS6 is correct
    - Check that the PVS6 is powered on
    - Check network connectivity

**Connection Refused or 403 Forbidden**
    - Check network connectivity
    - Try restarting the PVS6 device by disabling the breaker for it and then
      re-enabling it again.  The community has said that this works.

**Slow Response**
    - Increase timeout value
    - Check network performance

**Permission Errors**
    - Check file permissions for configuration files
    - Ensure proper user permissions

Best Practices
--------------

Output Format Selection
~~~~~~~~~~~~~~~~~~~~~~~

Choose appropriate output formats:

.. code-block:: bash

    # Use JSON for scripting and automation
    sungazer device list > devices.json

    # Use table for human reading
    sungazer --output table device list

    # Use table for monitoring
    sungazer --output table network list

Configuration Management
~~~~~~~~~~~~~~~~~~~~~~~~

Use configuration files when necessary.  The default configuration shipped
with ``sungazer`` is is typically fine if you are connecting directly to the
PVS6 itself, but you can override it with a configuration file.  See
:doc:`/overview/configuration` for more details.