"""Device management commands for Sungazer PVS6 API."""

import json

import click
from rich.console import Console
from rich.table import Table

from sungazer.cli.main import OddTypeEncoder, handle_exceptions


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

    if output_format == "json":
        click.echo(json.dumps(result.model_dump(), indent=2, cls=OddTypeEncoder))
    elif output_format == "table":
        console = Console()

        # Get the devices from the response
        devices_data = result.model_dump()
        devices = devices_data.get("devices", [])

        if not devices:
            console.print("No devices found")
            return

        # Create a table for each device
        for device in devices:
            # Create table with title and subtitle
            table = Table(
                title=f"{device.get('TYPE', 'Unknown')}: {device.get('MODEL', 'Unknown')}",
                caption=f"{device.get('SERIAL', 'Unknown Serial')}",
                show_header=True,
                header_style="bold magenta",
            )

            # Add columns
            table.add_column("Key", style="cyan", no_wrap=True)
            table.add_column("Value", style="green")

            # Add rows for each field in the device
            for key, value in device.items():
                if isinstance(value, (dict, list)):
                    formatted_value = json.dumps(value, indent=2, cls=OddTypeEncoder)
                else:
                    formatted_value = str(value)

                table.add_row(key, formatted_value)

            console.print(table)
            console.print()  # Add spacing between devices


@device.command(name="pvs", help="Get the PVS device information.")
@click.pass_context
@handle_exceptions
def get_pvs(ctx):
    """
    Get information about the PVS (Photovoltaic Supervisor) device.

    This command retrieves detailed information about the main PVS controller
    device, including system diagnostics, resource utilization, and operational
    metrics.

    Returns:
        PVS device information including:
        - System diagnostics and error counts
        - CPU load and memory usage
        - Flash storage availability
        - Network scan performance
        - System uptime and operational status
    """
    client = ctx.obj["client"]
    output_format = ctx.obj["output_format"]

    result = client.devices.list()
    pvs_device = result.pvs

    if output_format == "json":
        if pvs_device:
            click.echo(
                json.dumps(pvs_device.model_dump(), indent=2, cls=OddTypeEncoder)
            )
        else:
            click.echo(json.dumps({"error": "No PVS device found"}, indent=2))
    elif output_format == "table":
        console = Console()

        if not pvs_device:
            console.print("No PVS device found")
            return

        # Create table for PVS device
        table = Table(
            title=f"{pvs_device.TYPE}: {pvs_device.MODEL}",
            caption=f"{pvs_device.SERIAL}",
            show_header=True,
            header_style="bold magenta",
        )

        # Add columns
        table.add_column("Key", style="cyan", no_wrap=True)
        table.add_column("Value", style="green")

        # Add rows for each field
        device_data = pvs_device.model_dump()
        for key, value in device_data.items():
            if isinstance(value, (dict, list)):
                formatted_value = json.dumps(value, indent=2, cls=OddTypeEncoder)
            else:
                formatted_value = str(value)

            table.add_row(key, formatted_value)

        console.print(table)


@device.command(name="inverters", help="Get the list of inverter devices.")
@click.pass_context
@handle_exceptions
def get_inverters(ctx):
    """
    Get information about all inverter devices in the system.

    This command retrieves detailed information about all SolarBridge
    microinverters connected to the system, including power output,
    voltage/current measurements, and energy production data.

    Returns:
        Inverter information including:
        - AC power output and voltage/current measurements
        - DC input parameters from solar panels
        - Energy production totals
        - Temperature monitoring
        - Operational status and performance metrics
    """
    client = ctx.obj["client"]
    output_format = ctx.obj["output_format"]

    result = client.devices.list()
    inverters = result.inverters

    if output_format == "json":
        click.echo(
            json.dumps(
                [inv.model_dump() for inv in inverters], indent=2, cls=OddTypeEncoder
            )
        )
    elif output_format == "table":
        console = Console()

        if not inverters:
            console.print("No inverters found")
            return

        # Create a table for each inverter
        for inverter in inverters:
            table = Table(
                title=f"{inverter.TYPE}: {inverter.MODEL}",
                caption=f"{inverter.SERIAL}",
                show_header=True,
                header_style="bold magenta",
            )

            # Add columns
            table.add_column("Key", style="cyan", no_wrap=True)
            table.add_column("Value", style="green")

            # Add rows for each field
            device_data = inverter.model_dump()
            for key, value in device_data.items():
                if isinstance(value, (dict, list)):
                    formatted_value = json.dumps(value, indent=2, cls=OddTypeEncoder)
                else:
                    formatted_value = str(value)

                table.add_row(key, formatted_value)

            console.print(table)
            console.print()  # Add spacing between inverters


@device.command(name="production_meter", help="Get the production meter information.")
@click.pass_context
@handle_exceptions
def get_production_meter(ctx):
    """
    Get information about the production power meter.

    This command retrieves detailed information about the production power meter
    that measures solar energy generation, including power output, energy
    production, and electrical measurements.

    Returns:
        Production meter information including:
        - Real, reactive, and apparent power measurements
        - Energy production totals
        - Power factor and frequency
        - Voltage and current readings
        - Operational status and calibration data
    """
    client = ctx.obj["client"]
    output_format = ctx.obj["output_format"]

    result = client.devices.list()
    production_meter = result.production_meter

    if output_format == "json":
        if production_meter:
            click.echo(
                json.dumps(production_meter.model_dump(), indent=2, cls=OddTypeEncoder)
            )
        else:
            click.echo(json.dumps({"error": "No production meter found"}, indent=2))
    elif output_format == "table":
        console = Console()

        if not production_meter:
            console.print("No production meter found")
            return

        # Create table for production meter
        table = Table(
            title=f"{production_meter.TYPE}: {production_meter.MODEL}",
            caption=f"{production_meter.SERIAL}",
            show_header=True,
            header_style="bold magenta",
        )

        # Add columns
        table.add_column("Key", style="cyan", no_wrap=True)
        table.add_column("Value", style="green")

        # Add rows for each field
        device_data = production_meter.model_dump()
        for key, value in device_data.items():
            if isinstance(value, (dict, list)):
                formatted_value = json.dumps(value, indent=2, cls=OddTypeEncoder)
            else:
                formatted_value = str(value)

            table.add_row(key, formatted_value)

        console.print(table)


@device.command(name="consumption_meter", help="Get the consumption meter information.")
@click.pass_context
@handle_exceptions
def get_consumption_meter(ctx):
    """
    Get information about the consumption power meter.

    This command retrieves detailed information about the consumption power meter
    that measures site power usage, including power consumption, energy flow,
    and bidirectional measurements (import/export to utility grid).

    Returns:
        Consumption meter information including:
        - Power consumption measurements
        - Energy import/export totals
        - Multi-lead voltage and current readings
        - Power factor and frequency
        - Operational status and calibration data
    """
    client = ctx.obj["client"]
    output_format = ctx.obj["output_format"]

    result = client.devices.list()
    consumption_meter = result.consumption_meter

    if output_format == "json":
        if consumption_meter:
            click.echo(
                json.dumps(consumption_meter.model_dump(), indent=2, cls=OddTypeEncoder)
            )
        else:
            click.echo(json.dumps({"error": "No consumption meter found"}, indent=2))
    elif output_format == "table":
        console = Console()

        if not consumption_meter:
            console.print("No consumption meter found")
            return

        # Create table for consumption meter
        table = Table(
            title=f"{consumption_meter.TYPE}: {consumption_meter.MODEL}",
            caption=f"{consumption_meter.SERIAL}",
            show_header=True,
            header_style="bold magenta",
        )

        # Add columns
        table.add_column("Key", style="cyan", no_wrap=True)
        table.add_column("Value", style="green")

        # Add rows for each field
        device_data = consumption_meter.model_dump()
        for key, value in device_data.items():
            if isinstance(value, (dict, list)):
                formatted_value = json.dumps(value, indent=2, cls=OddTypeEncoder)
            else:
                formatted_value = str(value)

            table.add_row(key, formatted_value)

        console.print(table)
