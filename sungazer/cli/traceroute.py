import click

from sungazer.cli.main import handle_exceptions, output_formatter, read_json_file
from sungazer.models import TracerouteOptions


@click.group(name="traceroute")
def traceroute():
    """Traceroute operations."""


@traceroute.command(name="get-status")
@click.pass_context
@handle_exceptions
def get_status(ctx):
    """
    Get the status of the traceroute.

    Example:
        $ sungazer traceroute get-status

    """
    client = ctx.obj["client"]
    result = client.traceroute.get_status()
    output_formatter(result.model_dump(), ctx.obj["output_format"])


@traceroute.command(name="start")
@click.option(
    "--config-file",
    type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True),
    help="JSON file containing traceroute options",
)
@click.option("--destination", help="Destination to traceroute to")
@click.option("--hops", type=int, help="Maximum number of hops")
@click.option("--timeout", type=int, help="Timeout in seconds")
@click.pass_context
@handle_exceptions
def start_traceroute(ctx, config_file, destination, hops, timeout):
    """
    Start a traceroute.

    You can provide options either through a JSON file or through individual options.
    If both are provided, the file takes precedence.

    Example with file:
        $ sungazer traceroute start --config-file traceroute_options.json

    Example with options:
        $ sungazer traceroute start --destination 8.8.8.8 --hops 30 --timeout 2

    Example traceroute_options.json:
        {
          "destination": "8.8.8.8",
          "hops": 30,
          "timeout": 2
        }
    """
    client = ctx.obj["client"]

    if config_file:
        # Load from file
        config_data = read_json_file(config_file)
        options = TracerouteOptions(**config_data)
    else:
        # Build from options
        config_data = {}
        if destination:
            config_data["destination"] = destination
        if hops is not None:
            config_data["hops"] = hops
        if timeout is not None:
            config_data["timeout"] = timeout

        if not config_data or "destination" not in config_data:
            msg = "Either --config-file or at least --destination must be provided"
            raise click.UsageError(msg)

        options = TracerouteOptions(**config_data)

    result = client.traceroute.start(options)
    output_formatter(result.model_dump(), ctx.obj["output_format"])
