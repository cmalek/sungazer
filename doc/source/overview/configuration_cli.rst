Configuration: Command Line Tool
================================

This guide covers all configuration options for the ``sungazer`` command line tool, including
configuration files, environment variables, and command-line options.

In general the default values should work for most people if you are connecting
our computed directly to the PVS6 LAN1 port (or USB etherent dongle for newer
PVS6's). aside from the serial number of your PVS6.

We offer configuration files to change the default values to account for other
use cases, like using a Raspberry Pi as a proxy to the PVS6, and then connecting
to that proxy from your home network.

Configuration Methods
---------------------

The ``sungazer`` command line tool supports multiple configuration methods,
loaded in order of priority:

1. **Command-line options** (highest priority)
2. **Environment variables**
3. **Configuration files**
4. **Default values** (lowest priority)

Configuration Files
-------------------

File Locations
~~~~~~~~~~~~~~

Configuration files are searched in this order:

1. ``/etc/sungazer.conf`` (system-wide)
2. ``~/.sungazer.conf`` (user-specific)
3. ``./sungazer.conf`` (current directory)

File Format
~~~~~~~~~~~

Configuration files use INI format:

.. code-block:: ini

    [sungazer]
    base_url = http://sunpowerconsole.com/cgi-bin
    timeout = 30
    serial = ZT01234567890ABCDEF

Configuration Options
~~~~~~~~~~~~~~~~~~~~~

**base_url**
    The base URL for your PVS6 device API endpoint.

    Default: ``http://sunpowerconsole.com/cgi-bin``

    Example:
    .. code-block:: ini

        base_url = http://sunpowerconsole.com/cgi-bin

**timeout**
    Request timeout in seconds.

    Default: ``30``

    Example:

    .. code-block:: ini

        timeout = 60

**serial**
    The serial number of your PVS6 device.

    Default: ``None``

    Example:

    .. code-block:: ini

        serial = ZT01234567890ABCDEF

Environment Variables
---------------------

You can set configuration using environment variables:

.. code-block:: bash

    # Set base URL
    export SUNGAZER_BASE_URL="http://sunpowerconsole.com/cgi-bin"

    # Set timeout
    export SUNGAZER_TIMEOUT="30"

    # Set serial number
    export SUNGAZER_SERIAL="ZT01234567890ABCDEF"

Environment Variable Mapping
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- ``SUNGAZER_BASE_URL`` → ``base_url``
- ``SUNGAZER_TIMEOUT`` → ``timeout``
- ``SUNGAZER_SERIAL`` → ``serial``

Command-Line Options
--------------------

Global Options
~~~~~~~~~~~~~~

All commands support these global options:

.. code-block:: bash

    # Specify base URL
    sungazer --base-url http://sunpowerconsole.com/cgi-bin session start

    # Set timeout
    sungazer --timeout 60 device list

    # Choose output format
    sungazer --output table network list

Option Reference
~~~~~~~~~~~~~~~~

**--base-url**
    Override the base URL for API requests.

    Example:

    .. code-block:: bash

        sungazer --base-url https://sunpowerconsole.com/cgi-bin session start

**--timeout**
    Set request timeout in seconds.

    Example:

    .. code-block:: bash

        sungazer --timeout 120 device list

**--output**
    Choose output format: ``json`` or ``table``.

    Default: ``json``

    Example:
    .. code-block:: bash

        sungazer --output table device list

Configuration Examples
----------------------

Basic Setup
~~~~~~~~~~~

For a single PVS6 device:

.. code-block:: ini

    # ~/.sungazer.conf
    [sungazer]
    base_url = http://sunpowerconsole.com/cgi-bin
    timeout = 30
    serial = ZT01234567890ABCDEF

Multiple Devices
~~~~~~~~~~~~~~~~

For managing multiple devices, use environment variables or command-line options:

.. code-block:: bash

    # Device 1
    export SUNGAZER_BASE_URL="http://sunpowerconsole.com/cgi-bin"
    export SUNGAZER_SERIAL="ZT01234567890ABCDEF"
    sungazer session start

    # Device 2
    export SUNGAZER_BASE_URL="http://sunpowerconsole.com/cgi-bin"
    export SUNGAZER_SERIAL="ZT01234567890ABCDEG"
    sungazer session start

Or use command-line options:

.. code-block:: bash

    # Device 1
    sungazer --base-url http://sunpowerconsole.com/cgi-bin \
             --serial ZT01234567890ABCDEF \
             session start

    # Device 2
    sungazer --base-url http://sunpowerconsole.com/cgi-bin \
             --serial ZT01234567890ABCDEG \
             session start

Production Environment
~~~~~~~~~~~~~~~~~~~~~~

For production systems:

.. code-block:: ini

    # /etc/sungazer.conf
    [sungazer]
    base_url = https://sunpowerconsole.com/cgi-bin
    timeout = 60
    serial = ZT01234567890ABCDEF

Development Environment
~~~~~~~~~~~~~~~~~~~~~~~

For development and testing:

.. code-block:: ini

    # ~/.sungazer.conf
    [sungazer]
    base_url = http://sunpowerconsole.com/cgi-bin
    timeout = 10
    serial = ZT01234567890ABCDEF

Network-Specific Configuration
------------------------------

Local Network
~~~~~~~~~~~~~

For devices on your local network:

.. code-block:: ini

    [sungazer]
    base_url = http://sunpowerconsole.com/cgi-bin
    timeout = 30
    serial = ZT01234567890ABCDEF

Remote Access
~~~~~~~~~~~~~

For devices accessible over the internet:

.. code-block:: ini

    [sungazer]
    base_url = https://sunpowerconsole.com/cgi-bin
    timeout = 60
    serial = ZT01234567890ABCDEF

Slow Networks
~~~~~~~~~~~~~

For slow or unreliable networks:

.. code-block:: ini

    [sungazer]
    base_url = http://sunpowerconsole.com/cgi-bin
    timeout = 120
    serial = ZT01234567890ABCDEF

Security Considerations
-----------------------

Configuration File Security
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Protect your configuration files:

.. code-block:: bash

    # Set proper permissions
    chmod 600 ~/.sungazer.conf

    # For system-wide configuration
    chmod 640 /etc/sungazer.conf
    chown root:root /etc/sungazer.conf

Environment Variable Security
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Secure environment variable usage:

.. code-block:: bash

    # Set variables for current session only
    export SUNGAZER_BASE_URL="http://sunpowerconsole.com/cgi-bin"

    # Clear sensitive variables when done
    unset SUNGAZER_BASE_URL
    unset SUNGAZER_SERIAL

Troubleshooting Configuration
-----------------------------

Configuration Debugging
~~~~~~~~~~~~~~~~~~~~~~~

Check which configuration is being used:

.. code-block:: python

    from sungazer.cli.main import load_config

    # Load and display configuration
    config = load_config()
    print(f"Base URL: {config['base_url']}")
    print(f"Timeout: {config['timeout']}")
    print(f"Serial: {config['serial']}")

Common Issues
~~~~~~~~~~~~~

**API endpoint returning 403 Forbidden**
    - Power off the PVS6 and wait 10 seconds.  Then power it back on.  This seems to have worked for many people.

**sunpowerconsole.com not found**
    - On MacOS, ensure your ethernet device is listed first in the network list so that the nameserver running on the PVS6 is used first before the default nameserver.
    - On Linux, add ``nameserver 172.27.153.1`` to ``/etc/resolv.conf`` as the first nameserver.  This is the IP address of the PVS6 nameserver and webserver.
    - Not sure at this point if you need to do anything special for Windows.

**Configuration Not Loaded**
    - Check file permissions
    - Verify file format (INI syntax)
    - Ensure file is in correct location

**Configuration Not Valid**
    - See :ref:`Configuration Validation CLI` for more details.

**Environment Variables Not Recognized**
    - Check variable names (must start with ``SUNGAZER_``)
    - Restart terminal session
    - Verify variable values

**Command-Line Options Override**
    - Command-line options take highest priority
    - Check for conflicting options
    - Use ``--help`` to see current options


.. _Configuration Validation CLI:

Configuration Validation
------------------------

Validation Rules
~~~~~~~~~~~~~~~~

The library validates configuration:

- **base_url**: Must be a valid URL
- **timeout**: Must be a positive integer
- **serial**: Optional string

Error Messages
~~~~~~~~~~~~~~

Common validation errors:

.. code-block:: bash

    # Invalid URL
    Error: Invalid base_url format

    # Invalid timeout
    Error: Timeout must be a positive integer

    # Missing required field
    Error: base_url is required

Best Practices
--------------

Configuration Management
~~~~~~~~~~~~~~~~~~~~~~~~

1. **Use configuration files for defaults**

   - Set common settings in ``~/.sungazer.conf``
   - Use environment variables for overrides
   - Use command-line options for one-time changes

2. **Separate environments**

   - Use different config files for different environments
   - Use environment variables for sensitive data
   - Document configuration requirements

3. **Version control**

   - Don't commit sensitive configuration
   - Use templates for configuration files
   - Document configuration changes

4. **Security**

   - Protect configuration files with proper permissions
   - Use HTTPS when available
   - Clear sensitive environment variables

5. **Testing**

   - Test timeout settings

Configuration Templates
-----------------------

Basic Template
~~~~~~~~~~~~~~

.. code-block:: ini

    # sungazer.conf.template
    [sungazer]
    base_url = http://sunpowerconsole.com/cgi-bin

    # Request timeout in seconds
    timeout = 30

    # Your device's serial number (optional)
    serial = ZT01234567890ABCDEF

Production Template
~~~~~~~~~~~~~~~~~~~

.. code-block:: ini

    # sungazer.production.conf
    [sungazer]
    base_url = https://sunpowerconsole.com/cgi-bin

    # Longer timeout for production
    timeout = 60

    # Production device serial
    serial = ZT01234567890ABCDEF

Development Template
~~~~~~~~~~~~~~~~~~~~

.. code-block:: ini

    # sungazer.dev.conf
    [sungazer]
    base_url = http://sunpowerconsole.com/cgi-bin
    timeout = 10
    serial = ZT01234567890ABCDEF