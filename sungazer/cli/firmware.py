import click

from sungazer.cli.main import handle_exceptions, output_formatter


@click.group(name="firmware")
def firmware():
    """Firmware operations."""


@firmware.command(name="get-info")
@click.pass_context
@handle_exceptions
def get_info(ctx):
    """
    Get firmware information.

    Example:
        $ sungazer firmware get-info

    """
    client = ctx.obj["client"]
    result = client.firmware.get_info()
    output_formatter(result.model_dump(), ctx.obj["output_format"])


@firmware.command(name="start-update")
@click.option("--url", required=True, help="URL to download the firmware from")
@click.option("--version", required=True, help="Version of the firmware")
@click.pass_context
@handle_exceptions
def start_update(ctx, url, version):
    """
    Start a firmware update.

    Example:
        $ sungazer firmware start-update \
            --url https://example.com/firmware.bin \
            --version 1.2.3

    """
    client = ctx.obj["client"]
    result = client.firmware.start_update(url, version)
    output_formatter(result.model_dump(), ctx.obj["output_format"])
