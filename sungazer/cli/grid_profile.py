import click

from sungazer.cli.main import handle_exceptions, output_formatter


@click.group(name="grid-profile")
def grid_profile():
    """Grid profile operations."""


@grid_profile.command(name="get-list")
@click.pass_context
@handle_exceptions
def get_list(ctx):
    """
    Get the list of grid profiles.

    Example:
        $ sungazer grid-profile get-list

    """
    client = ctx.obj["client"]
    result = client.grid_profiles.get_list()
    output_formatter([p.model_dump() for p in result], ctx.obj["output_format"])


@grid_profile.command(name="get-status")
@click.pass_context
@handle_exceptions
def get_status(ctx):
    """
    Get the grid profile status.

    Example:
        $ sungazer grid-profile get-status

    """
    client = ctx.obj["client"]
    result = client.grid_profiles.get_status()
    output_formatter(result.model_dump(), ctx.obj["output_format"])


@grid_profile.command(name="set-profile")
@click.argument("grid-profile-id")
@click.pass_context
@handle_exceptions
def set_profile(ctx, grid_profile_id: str):  # noqa: D417
    """
    Set the grid profile.

    Args:
        GRID_PROFILE_ID: The grid profile ID

    Example:
        $ sungazer grid-profile set-profile 123

    """
    client = ctx.obj["client"]
    result = client.grid_profiles.set_profile(grid_profile_id)
    output_formatter(result.model_dump(), ctx.obj["output_format"])
