import click

from sungazer.cli.main import handle_exceptions, output_formatter, read_json_file
from sungazer.models import PingOptions


@click.group(name="ping")
def ping():
    """Ping operations."""


@ping.command(name="get-status")
@click.pass_context
@handle_exceptions
def get_status(ctx):
    """
    Get the status of the ping.

    Example:
        $ sungazer ping get-status

    """
    client = ctx.obj["client"]
    result = client.ping.get_status()
    output_formatter(result.model_dump(), ctx.obj["output_format"])


@ping.command(name="start")
@click.option(
    "--config-file",
    type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True),
    help="JSON file containing ping options",
)
@click.option("--destination", help="Destination to ping")
@click.option("--count", type=int, help="Number of ping packets to send")
@click.option("--size", type=int, help="Size of ping packets")
@click.option("--interval", type=float, help="Interval between pings in seconds")
@click.option("--timeout", type=int, help="Timeout in seconds")
@click.option("--ttl", type=int, help="Time to live")
@click.pass_context
@handle_exceptions
def start_ping(ctx, config_file, destination, count, size, interval, timeout, ttl):
    """
    Start a ping.

    You can provide options either through a JSON file or through individual options.
    If both are provided, the file takes precedence.

    Example with file:
        $ sungazer ping start --config-file ping_options.json

    Example with options:
        $ sungazer ping start \
            --destination 8.8.8.8 \
            --count 5 \
            --size 56 \
            --interval 1 \
            --timeout 2 \
            --ttl 64

    Example ping_options.json:
        {
          "destination": "8.8.8.8",
          "count": 5,
          "size": 56,
          "interval": 1,
          "timeout": 2,
          "ttl": 64
        }
    """
    client = ctx.obj["client"]

    if config_file:
        # Load from file
        config_data = read_json_file(config_file)
        options = PingOptions(**config_data)
    else:
        # Build from options
        config_data = {}
        if destination:
            config_data["destination"] = destination
        if count is not None:
            config_data["count"] = count
        if size is not None:
            config_data["size"] = size
        if interval is not None:
            config_data["interval"] = interval
        if timeout is not None:
            config_data["timeout"] = timeout
        if ttl is not None:
            config_data["ttl"] = ttl

        if not config_data or "destination" not in config_data:
            msg = "Either --config-file or at least --destination must be provided"
            raise click.UsageError(msg)

        options = PingOptions(**config_data)

    result = client.ping.start(options)
    output_formatter(result.model_dump(), ctx.obj["output_format"])
