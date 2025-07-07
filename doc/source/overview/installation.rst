Installation
============

This guide covers how to install the ``sungazer`` library and its dependencies.

Prerequisites
-------------

Before installing ``sungazer``, ensure you have:

- Python 3.10 or higher
- `uv <https://docs.astral.sh/uv/>`_ or `pip <https://pip.pypa.io/en/stable/>`_
- Access to a SunPower PVS6 device and a way to connect to it (see :doc:`/overview/connecting`)

Installation Methods
--------------------

From PyPI with ``pip``
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    python -m venv .venv
    source .venv/bin/activate
    pip install sungazer

From PyPI with ``uv``
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    sh -c "$(curl -fsSL https://astral.sh/uv/install)"
    uv tool install sungazer
    # Ensure you have ./local/bin in your PATH, since that's where uv puts the
    # executable
    sungazer --help


From Source
~~~~~~~~~~~

If you want to install from the latest development version:

.. code-block:: bash

    git clone https://github.com/cmalek/sungazer.git
    sh -c "$(curl -fsSL https://astral.sh/uv/install)"
    cd sungazer
    uv tool install .

Verification
------------

After installation, verify that ``sungazer`` is properly installed:

.. code-block:: python

    source .venv/bin/activate
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

    sh -c "$(curl -fsSL https://astral.sh/uv/install)"
    git clone https://github.com/your-repo/sungazer.git
    cd sungazer
    uv sync --dev

This installs additional development dependencies including:

- **pytest**: Testing framework
- **mypy**: Static type checker
- **black**: Code formatter
- **ruff**: Fast Python linter

Configuration
-------------

After installation, you may want to configure ``sungazer`` for your specific PVS6 device.
See :doc:`configuration` for detailed configuration options.

Getting Help
------------

If you encounter issues during installation:

1. Check the `GitHub issues <https://github.com/your-repo/sungazer/issues>`_
2. Review the troubleshooting section above
3. Ensure your Python environment meets the prerequisites
4. Try installing in a virtual environment to isolate dependencies