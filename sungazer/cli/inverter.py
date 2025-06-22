import click

from sungazer.cli.main import handle_exceptions, output_formatter


@click.group(name="inverter")
def inverter():
    """Inverter operations."""


@inverter.command(name="get-list")
@click.pass_context
@handle_exceptions
def get_list(ctx):
    """
    Get the inverters.

    Example:
        $ sungazer inverter get-list

    """
    client = ctx.obj["client"]
    result = client.inverters.get_list()
    output_formatter(result.model_dump(), ctx.obj["output_format"])
