Installation
============

This guide covers how to install the ``sungazer`` library and its dependencies.

Prerequisites
-------------

Before installing ``sungazer``, ensure you have:

- Python 3.8 or higher
- pip (Python package installer)
- Access to a SunPower PVS6 device on your network

Installation Methods
--------------------

From PyPI (Recommended)
~~~~~~~~~~~~~~~~~~~~~~~

The easiest way to install ``sungazer`` is using pip:

.. code-block:: bash

    pip install sungazer

From Source
~~~~~~~~~~~

If you want to install from the latest development version:

.. code-block:: bash

    git clone https://github.com/your-repo/sungazer.git
    cd sungazer
    pip install -e .

Using uv (Fast Python Package Installer)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you prefer using `uv <https://github.com/astral-sh/uv>`_ for faster package management:

.. code-block:: bash

    uv add sungazer

Verification
------------

After installation, verify that ``sungazer`` is properly installed:

.. code-block:: python

    python -c "import sungazer; print(sungazer.__version__)"

You should also be able to run the CLI:

.. code-block:: bash

    sungazer --help

Dependencies
------------

``sungazer`` has the following key dependencies:

- **httpx**: Modern HTTP client for Python
- **pydantic**: Data validation using Python type annotations
- **click**: Command line interface creation kit
- **rich**: Rich text and beautiful formatting in the terminal

These dependencies are automatically installed when you install ``sungazer``.

Development Installation
------------------------

If you plan to contribute to ``sungazer`` or need the latest development features:

.. code-block:: bash

    git clone https://github.com/your-repo/sungazer.git
    cd sungazer
    pip install -e ".[dev]"

This installs additional development dependencies including:

- **pytest**: Testing framework
- **mypy**: Static type checker
- **black**: Code formatter
- **ruff**: Fast Python linter

Configuration
-------------

After installation, you may want to configure ``sungazer`` for your specific PVS6 device.
See :doc:`configuration` for detailed configuration options.

Troubleshooting
---------------

Common Installation Issues
~~~~~~~~~~~~~~~~~~~~~~~~~~

**Permission Errors**
    If you encounter permission errors during installation, try:

    .. code-block:: bash

        pip install --user sungazer

**SSL Certificate Issues**
    If you have SSL certificate issues with your PVS6 device, the library is
    configured to handle this automatically by disabling SSL verification.

**Network Connectivity**
    Ensure your PVS6 device is accessible on your network and the API endpoint
    is reachable from your machine.

Getting Help
------------

If you encounter issues during installation:

1. Check the `GitHub issues <https://github.com/your-repo/sungazer/issues>`_
2. Review the troubleshooting section above
3. Ensure your Python environment meets the prerequisites
4. Try installing in a virtual environment to isolate dependencies