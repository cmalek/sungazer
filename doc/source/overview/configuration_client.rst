Configuration: Python Client
============================

This guide covers all configuration options for the ``sungazer`` Python client.

Direct Configuration
~~~~~~~~~~~~~~~~~~~~

Configure the client directly in Python:

.. code-block:: python

    from sungazer import SungazerClient

    # Basic configuration
    client = SungazerClient(
        base_url="http://sunpowerconsole.com/cgi-bin",
        timeout=30,
        serial="ZT01234567890ABCDEF"
    )

Advanced Configuration
~~~~~~~~~~~~~~~~~~~~~~

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


SSL Configuration
-----------------

SSL Certificate Handling
~~~~~~~~~~~~~~~~~~~~~~~~

The library automatically handles SSL certificate issues by disabling verification.
For custom SSL configuration:

.. code-block:: python

    import httpx
    from sungazer import SungazerClient

    # Custom SSL configuration
    http_client = httpx.Client(
        verify=False,  # Disable SSL verification
        timeout=httpx.Timeout(30.0)
    )

    client = SungazerClient(
        base_url="https://sunpowerconsole.com/cgi-bin",
        client=http_client
    )

Troubleshooting Configuration
-----------------------------

Common Issues
~~~~~~~~~~~~~

**API endpoint returning 403 Forbidden**
    - Power off the PVS6 and wait 10 seconds.  Then power it back on.  This seems to have worked for many people.

**sunpowerconsole.com not found**
    - On MacOS, ensure your ethernet device is listed first in the network list so that the nameserver running on the PVS6 is used first before the default nameserver.
    - On Linux, add ``nameserver 172.27.153.1`` to ``/etc/resolv.conf`` as the first nameserver.  This is the IP address of the PVS6 nameserver and webserver.
    - Not sure at this point if you need to do anything special for Windows.

**Configuration Not Valid**
    - See :ref:`Configuration Validation Client` for more details.


.. _Configuration Validation Client:

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
