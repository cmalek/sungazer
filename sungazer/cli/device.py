"""Device management commands for Sungazer PVS6 API."""

import click

from sungazer.cli.main import handle_exceptions, output_formatter


@click.group(help="Device information commands.")
def device():
    """
    Device management commands.

    These commands allow you to discover and manage devices connected to the
    Sungazer PVS6 system, including inverters, batteries, and other components.
    """


@device.command(name="list", help="Get the list of connected devices.")
@click.pass_context
@handle_exceptions
def list_devices(ctx):
    """
    Get the device discovery progress and list of connected devices.

    This command retrieves information about all devices discovered by the
    Sungazer PVS6 system, including their types, status, and configuration
    details.

    Returns:
        Device information including:
        - Device types (inverters, batteries, gateways, etc.)
        - Device status and operational state
        - Configuration and firmware information
        - Discovery progress and connection details

    """
    client = ctx.obj["client"]
    output_format = ctx.obj["output_format"]

    result = client.devices.list()
    output_formatter(result.model_dump(), output_format)
