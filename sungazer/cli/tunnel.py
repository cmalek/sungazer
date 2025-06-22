import click

from sungazer.cli.main import handle_exceptions, output_formatter, read_json_file
from sungazer.models import TunnelOptions


@click.group(name="tunnel")
def tunnel():
    """Tunnel operations."""


@tunnel.command(name="get-status")
@click.pass_context
@handle_exceptions
def get_status(ctx):
    """
    Get the status of the SSH tunnel.

    Example:
        $ sungazer tunnel get-status

    """
    client = ctx.obj["client"]
    result = client.tunnel.get_status()
    output_formatter(result.model_dump(), ctx.obj["output_format"])


@tunnel.command(name="start")
@click.option(
    "--config-file",
    type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True),
    help="JSON file containing tunnel options",
)
@click.option("--duration", type=int, help="Duration of the tunnel in minutes")
@click.option("--server", help="Tunnel server address")
@click.option("--local-port", type=int, help="Local port to use")
@click.option("--remote-port", type=int, help="Remote port to use")
@click.pass_context
@handle_exceptions
def start_tunnel(ctx, config_file, duration, server, local_port, remote_port):
    """
    Start an SSH tunnel.

    You can provide options either through a JSON file or through individual options.
    If both are provided, the file takes precedence.

    Example with file:
        $ sungazer tunnel start --config-file tunnel_options.json

    Example with options:
        $ sungazer tunnel start \
            --duration 60 \
            --server ssh.example.com \
            --local-port 22 \
            --remote-port 2222

    Example tunnel_options.json:
        {
          "duration": 60,
          "server": "ssh.example.com",
          "localPort": 22,
          "remotePort": 2222
        }
    """
    client = ctx.obj["client"]

    if config_file:
        # Load from file
        config_data = read_json_file(config_file)
        options = TunnelOptions(**config_data)
    else:
        # Build from options
        config_data = {}
        if duration is not None:
            config_data["duration"] = duration
        if server:
            config_data["server"] = server
        if local_port is not None:
            config_data["localPort"] = local_port
        if remote_port is not None:
            config_data["remotePort"] = remote_port

        if not config_data or not all(k in config_data for k in ["duration", "server"]):
            msg = (
                "Either --config-file or at least --duration and --server must be "
                "provided"
            )
            raise click.UsageError(msg)

        options = TunnelOptions(**config_data)

    result = client.tunnel.start(options)
    output_formatter(result.model_dump(), ctx.obj["output_format"])


@tunnel.command(name="delete-all")
@click.pass_context
@handle_exceptions
def delete_all(ctx):
    """
    Delete all SSH tunnels.

    Example:
        $ sungazer tunnel delete-all

    """
    client = ctx.obj["client"]
    result = client.tunnel.delete_all()
    output_formatter(result.model_dump(), ctx.obj["output_format"])
