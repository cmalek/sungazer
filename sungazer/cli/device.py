import click

from sungazer.cli.main import handle_exceptions, output_formatter, read_json_file
from sungazer.enums import ClaimOpEnum
from sungazer.models import ClaimOperation, ClaimOperationList


@click.group(name="device")
def device():
    """Device operations."""


@device.command(name="get-discovery-progress")
@click.pass_context
@handle_exceptions
def get_discovery_progress(ctx):
    """
    Get the discovery progress.

    Example:
        $ sungazer device get-discovery-progress

    """
    client = ctx.obj["client"]
    result = client.devices.get_discovery_progress()
    output_formatter(result.model_dump(), ctx.obj["output_format"])


@device.command(name="start-discovery")
@click.option(
    "--num-devices", type=int, default=200, help="Number of devices to discover"
)
@click.option(
    "--mi-type",
    type=click.Choice(["ALL", "ENPH", "SBT"]),
    default="ALL",
    help="MI type",
)
@click.option(
    "--device-type",
    default="all",
    help="Device type (allnomi, all, Metstation, allplusmime, allnoinverters, storage)",
)
@click.option(
    "--interface",
    multiple=True,
    help="Interface to use (mime, net, ttyUSB0, ttyUSB1, ttyUSB2, local)",
)
@click.option("--save-config/--no-save-config", default=False, help="Save config file")
@click.option("--keep-devices/--no-keep-devices", default=False, help="Keep devices")
@click.pass_context
@handle_exceptions
def start_discovery(
    ctx, num_devices, mi_type, device_type, interface, save_config, keep_devices
):
    """
    Start discovering devices.

    Example:
        $ sungazer device start-discovery \
            --num-devices 100 \
            --mi-type ALL \
            --device-type all \
            --interface mime \
            --interface net \
            --save-config \
            --keep-devices

    """
    client = ctx.obj["client"]
    interfaces = list(interface) if interface else None
    result = client.devices.start_discovery(
        num_devices=num_devices,
        mi_type=mi_type,
        device=device_type,
        interfaces=interfaces,
        save_config_file=save_config,
        keep_devices=keep_devices,
    )
    output_formatter(result.model_dump(), ctx.obj["output_format"])


@device.command(name="get-list")
@click.option(
    "--detailed/--no-detailed", default=False, help="Include detailed information"
)
@click.pass_context
@handle_exceptions
def get_list(ctx, detailed):
    """
    Get the device list.

    Example:
        $ sungazer device get-list --detailed

    """
    client = ctx.obj["client"]
    result = client.devices.get_list(detailed=detailed)
    output_formatter(result.model_dump(), ctx.obj["output_format"])


@device.command(name="start-claim")
@click.option(
    "--operations-file",
    type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True),
    help="JSON file containing claim operations",
)
@click.option("--add", is_flag=True, help="Add operation")
@click.option("--delete", is_flag=True, help="Delete operation")
@click.option("--noop", is_flag=True, help="No operation")
@click.option("--model", help="Model type of the device")
@click.option("--serial", help="Serial number of the device")
@click.option("--device-type", help="Device type")
@click.pass_context
@handle_exceptions
def start_claim(ctx, operations_file, add, delete, noop, model, serial, device_type):
    """
    Start claiming devices.

    You can provide operations either through a JSON file or through individual options.
    If both are provided, the file takes precedence.

    Example with file:
        $ sungazer device start-claim --operations-file operations.json

    Example with options:
        $ sungazer device start-claim \
            --add \
            --model PVS6M0400p \
            --serial ZT123456 \
            --device-type PVS5-METER-P

    Example operations.json:
        [
          {
            "OPERATION": "add",
            "MODEL": "PVS6M0400p",
            "SERIAL": "ZT123456",
            "TYPE": "PVS5-METER-P"
          }
        ]
    """
    client = ctx.obj["client"]

    if operations_file:
        # Load from file
        operations_data = read_json_file(operations_file)
        operations = ClaimOperationList(__root__=operations_data)
    else:
        # Build from options
        if not (add or delete or noop):
            msg = "One of --add, --delete, or --noop must be specified"
            raise click.UsageError(msg)

        if not (model and serial and device_type):
            msg = "--model, --serial, and --device-type must be specified"
            raise click.UsageError(msg)

        operation = (
            ClaimOpEnum.add
            if add
            else ClaimOpEnum.delete
            if delete
            else ClaimOpEnum.noop
        )

        operation_data = {
            "OPERATION": operation,
            "MODEL": model,
            "SERIAL": serial,
            "TYPE": device_type,
        }

        operations = ClaimOperationList(__root__=[ClaimOperation(**operation_data)])

    result = client.devices.start_claim(operations)
    output_formatter(result.model_dump(), ctx.obj["output_format"])


@device.command(name="get-claim-progress")
@click.pass_context
@handle_exceptions
def get_claim_progress(ctx):
    """
    Get the claim progress.

    Example:
        $ sungazer device get-claim-progress

    """
    client = ctx.obj["client"]
    result = client.devices.get_claim_progress()
    output_formatter(result.model_dump(), ctx.obj["output_format"])
