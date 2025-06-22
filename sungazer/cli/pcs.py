import click

from sungazer.cli.main import handle_exceptions, output_formatter, read_json_file
from sungazer.models import PCSSettings


@click.group(name="pcs")
def pcs():
    """PCS operations."""


@pcs.command(name="get-settings")
@click.pass_context
@handle_exceptions
def get_settings(ctx):
    """
    Get the PCS settings.

    Example:
        $ sungazer pcs get-settings

    """
    client = ctx.obj["client"]
    result = client.pcs.get_settings()
    output_formatter(result.model_dump(), ctx.obj["output_format"])


@pcs.command(name="update-settings")
@click.option(
    "--config-file",
    type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True),
    required=True,
    help="JSON file containing PCS settings",
)
@click.pass_context
@handle_exceptions
def update_settings(ctx, config_file):
    """
    Update the PCS settings.

    Example:
        $ sungazer pcs update-settings --config-file pcs_settings.json

    Example pcs_settings.json:
        {
          "enableStorage": true,
          "exportLimit": 5000,
          "enableCharging": true,
          "enableGridSupport": true
        }

    """
    client = ctx.obj["client"]

    # Load from file
    config_data = read_json_file(config_file)
    settings = PCSSettings(**config_data)

    result = client.pcs.update_settings(settings)
    output_formatter(result.model_dump(), ctx.obj["output_format"])
