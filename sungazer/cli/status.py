import click

from sungazer.cli.main import handle_exceptions, output_formatter


@click.group(name="status")
def status():
    """Status operations."""


@status.command(name="get-ess")
@click.pass_context
@handle_exceptions
def get_ess(ctx):
    """
    Get the energy storage system status.

    Example:
        $ sungazer status get-ess

    """
    client = ctx.obj["client"]
    result = client.status.get_ess()
    output_formatter(result.model_dump(), ctx.obj["output_format"])


@status.command(name="get-equinox")
@click.pass_context
@handle_exceptions
def get_equinox(ctx):
    """
    Get the Equinox system status.

    Example:
        $ sungazer status get-equinox

    """
    client = ctx.obj["client"]
    result = client.status.get_equinox()
    output_formatter(result.model_dump(), ctx.obj["output_format"])
