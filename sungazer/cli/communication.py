import click

from sungazer.cli.main import handle_exceptions, output_formatter


@click.group(name="communication")
def communication():
    """Communication operations."""


@communication.command(name="get-interfaces")
@click.pass_context
@handle_exceptions
def get_interfaces(ctx):
    """
    Get all information for all communications interfaces.

    Example:
        $ sungazer communication get-interfaces

    """
    client = ctx.obj["client"]
    result = client.communication.get_interfaces()
    output_formatter(result.model_dump(), ctx.obj["output_format"])


@communication.command(name="scan-wifi")
@click.pass_context
@handle_exceptions
def scan_wifi(ctx):
    """
    Scan for WiFi networks.

    Example:
        $ sungazer communication scan-wifi

    """
    client = ctx.obj["client"]
    result = client.communication.scan_wifi()
    output_formatter(result.model_dump(), ctx.obj["output_format"])


@communication.command(name="get-p2p-pairing-info")
@click.pass_context
@handle_exceptions
def get_p2p_pairing_info(ctx):
    """
    Get P2P pairing information.

    Example:
        $ sungazer communication get-p2p-pairing-info

    """
    client = ctx.obj["client"]
    result = client.communication.get_p2p_pairing_info()
    output_formatter(result.model_dump(), ctx.obj["output_format"])


@communication.command(name="pair-p2p-client")
@click.argument("client_name")
@click.pass_context
@handle_exceptions
def pair_p2p_client(ctx, client_name):
    """
    Pair a P2P client.

    Args:
        CLIENT_NAME: The client name

    Example:
        $ sungazer communication pair-p2p-client my-client

    """
    client = ctx.obj["client"]
    result = client.communication.pair_p2p_client(client_name)
    output_formatter(result.model_dump(), ctx.obj["output_format"])
