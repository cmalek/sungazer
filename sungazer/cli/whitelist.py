import click

from sungazer.cli.main import handle_exceptions, output_formatter, read_json_file
from sungazer.models import Whitelist


@click.group(name="whitelist")
def whitelist():
    """Whitelist operations."""


@whitelist.command(name="get")
@click.pass_context
@handle_exceptions
def get(ctx):
    """
    Get the whitelist.

    Example:
        $ sungazer whitelist get

    """
    client = ctx.obj["client"]
    result = client.whitelist.get()
    output_formatter(result.model_dump(), ctx.obj["output_format"])


@whitelist.command(name="update")
@click.option(
    "--config-file",
    type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True),
    required=True,
    help="JSON file containing whitelist",
)
@click.pass_context
@handle_exceptions
def update(ctx, config_file):
    """
    Update the whitelist.

    Example:
        $ sungazer whitelist update --config-file whitelist.json

    Example whitelist.json:
        {
          "whitelist": [
            "192.168.1.100",
            "192.168.1.101"
          ]
        }

    """
    client = ctx.obj["client"]

    # Load from file
    config_data = read_json_file(config_file)
    whitelist_data = Whitelist(**config_data)

    result = client.whitelist.update(whitelist_data)
    output_formatter(result.model_dump(), ctx.obj["output_format"])
