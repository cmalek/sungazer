import click

from sungazer.cli.main import handle_exceptions, output_formatter, read_json_file
from sungazer.enums import PowerProduction
from sungazer.models import (
    FirewallSettingsConfiguration,
    GeneralSettings,
    InterfaceConfiguration,
    PowerProductionSetting,
)


@click.group(name="network")
def network():
    """Network operations."""


@network.command(name="renew-dhcp-lease")
@click.argument("network_type", type=click.Choice(["eth", "wifi", "plc"]))
@click.pass_context
@handle_exceptions
def renew_dhcp_lease(ctx, network_type: str):  # noqa: D417
    """
    Renew the DHCP lease for the specified network type.

    Args:
        NETWORK_TYPE: The network type (eth, wifi, plc)

    Example:
        $ sungazer network renew-dhcp-lease eth

    """
    client = ctx.obj["client"]
    result = client.network.renew_dhcp_lease(network_type)
    output_formatter(result.model_dump(), ctx.obj["output_format"])


@network.command(name="release-dhcp-lease")
@click.argument("network_type", type=click.Choice(["eth", "wifi", "plc"]))
@click.pass_context
@handle_exceptions
def release_dhcp_lease(ctx, network_type: str):  # noqa: D417
    """
    Release the DHCP lease for the specified network type.

    Args:
        NETWORK_TYPE: The network type (eth, wifi, plc)

    Example:
        $ sungazer network release-dhcp-lease eth

    """
    client = ctx.obj["client"]
    result = client.network.release_dhcp_lease(network_type)
    output_formatter(result.model_dump(), ctx.obj["output_format"])


@network.command(name="get-power-production")
@click.pass_context
@handle_exceptions
def get_power_production(ctx):
    """
    Get the power production status.

    Example:
        $ sungazer network get-power-production

    """
    client = ctx.obj["client"]
    result = client.network.get_power_production()
    output_formatter(result.model_dump(), ctx.obj["output_format"])


@network.command(name="set-power-production")
@click.option("--on/--off", required=True, help="Turn power production on or off")
@click.pass_context
@handle_exceptions
def set_power_production(ctx, on):
    """
    Set the power production status.

    Example:
        $ sungazer network set-power-production --on
        $ sungazer network set-power-production --off

    """
    client = ctx.obj["client"]
    settings = PowerProductionSetting(
        powerProduction=PowerProduction.On if on else PowerProduction.Off
    )
    result = client.network.set_power_production(settings)
    output_formatter(result.model_dump(), ctx.obj["output_format"])


@network.command(name="start-cell-primary-check")
@click.argument("address")
@click.pass_context
@handle_exceptions
def start_cell_primary_check(ctx, address: str):  # noqa: D417
    """
    Begin checking for permission to set cellular as a primary network interface.

    Args:
        ADDRESS: The address to look up

    Example:
        $ sungazer network start-cell-primary-check 192.168.1.1

    """
    client = ctx.obj["client"]
    result = client.network.start_cell_primary_check(address)
    output_formatter(result.model_dump(), ctx.obj["output_format"])


@network.command(name="get-interface-config")
@click.argument("network_type", type=click.Choice(["eth", "wifi", "plc"]))
@click.pass_context
@handle_exceptions
def get_interface_config(ctx, network_type: str):  # noqa: D417
    """
    Get the interface configuration.

    Args:
        NETWORK_TYPE: The network type (eth, wifi, plc)

    Example:
        $ sungazer network get-interface-config eth

    """
    client = ctx.obj["client"]
    result = client.network.get_interface_config(network_type)
    output_formatter(result.model_dump(), ctx.obj["output_format"])


@network.command(name="update-interface-config")
@click.argument("network_type", type=click.Choice(["eth", "wifi", "plc"]))
@click.option(
    "--config-file",
    type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True),
    help="JSON file containing interface configuration",
)
@click.option(
    "--network-type-value",
    type=click.Choice(["PLC", "ETH", "WIFI"]),
    help="Network type",
)
@click.option(
    "--configuration-type",
    type=click.Choice(["DHCP", "STATIC"]),
    help="Configuration type",
)
@click.option("--ip-address", help="IP address")
@click.option("--subnet-mask", help="Subnet mask")
@click.option("--gateway", help="Gateway")
@click.option("--dns-server", help="DNS server")
@click.pass_context
@handle_exceptions
def update_interface_config(  # noqa: D417
    ctx,
    network_type,
    config_file,
    network_type_value,
    configuration_type,
    ip_address,
    subnet_mask,
    gateway,
    dns_server,
):
    """
    Update the interface configuration.

    Args:
        NETWORK_TYPE: The network type (eth, wifi, plc)

    You can provide configuration either through a JSON file or through
    individual options.  If both are provided, the file takes precedence.

    Example with file:
        $ sungazer network update-interface-config eth --config-file config.json

    Example with options:
        $ sungazer network update-interface-config eth \
            --network-type-value ETH \
            --configuration-type STATIC \
            --ip-address 192.168.1.100 \
            --subnet-mask 255.255.255.0 \
            --gateway 192.168.1.1 \
            --dns-server 8.8.8.8

    Example config.json:
        {
          "networkType": "ETH",
          "configurationType": "STATIC",
          "ipAddress": "192.168.1.100",
          "subnetMask": "255.255.255.0",
          "gateway": "192.168.1.1",
          "dnsServer": "8.8.8.8"
        }

    """
    client = ctx.obj["client"]

    if config_file:
        # Load from file
        config_data = read_json_file(config_file)
        config = InterfaceConfiguration(**config_data)
    else:
        # Build from options
        config_data = {}
        if network_type_value:
            config_data["networkType"] = network_type_value
        if configuration_type:
            config_data["configurationType"] = configuration_type
        if ip_address:
            config_data["ipAddress"] = ip_address
        if subnet_mask:
            config_data["subnetMask"] = subnet_mask
        if gateway:
            config_data["gateway"] = gateway
        if dns_server:
            config_data["dnsServer"] = dns_server

        if not config_data:
            msg = (
                "Either --config-file or individual configuration options must "
                "be provided"
            )
            raise click.UsageError(msg)

        config = InterfaceConfiguration(**config_data)

    result = client.network.update_interface_config(network_type, config)
    output_formatter(result.model_dump(), ctx.obj["output_format"])


@network.command(name="get-firewall-settings")
@click.pass_context
@handle_exceptions
def get_firewall_settings(ctx):
    """
    Get the firewall settings.

    Example:
        $ sungazer network get-firewall-settings

    """
    client = ctx.obj["client"]
    result = client.network.get_firewall_settings()
    output_formatter(result.model_dump(), ctx.obj["output_format"])


@network.command(name="update-firewall-settings")
@click.option(
    "--config-file",
    type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True),
    required=True,
    help="JSON file containing firewall settings",
)
@click.pass_context
@handle_exceptions
def update_firewall_settings(ctx, config_file):
    """
    Update the firewall settings.

    Example:
        $ sungazer network update-firewall-settings --config-file firewall_settings.json

    Example firewall_settings.json:
        {
          "FirewallSettings": [
            {
              "firewallSettingsId": "ssh",
              "external": {
                "device": "wan",
                "port": "22"
              },
              "internal": {
                "device": "localhost",
                "port": "22"
              },
              "protocol": "tcp",
              "enable": true
            }
          ]
        }

    """
    client = ctx.obj["client"]

    # Load from file
    config_data = read_json_file(config_file)
    config = FirewallSettingsConfiguration(**config_data)

    result = client.network.update_firewall_settings(config)
    output_formatter(result.model_dump(), ctx.obj["output_format"])


@network.command(name="get-network-settings")
@click.pass_context
@handle_exceptions
def get_network_settings(ctx):
    """
    Get the network settings.

    Example:
        $ sungazer network get-network-settings

    """
    client = ctx.obj["client"]
    result = client.network.get_network_settings()
    output_formatter(result.model_dump(), ctx.obj["output_format"])


@network.command(name="update-network-settings")
@click.option(
    "--config-file",
    type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True),
    required=True,
    help="JSON file containing network settings",
)
@click.pass_context
@handle_exceptions
def update_network_settings(ctx, config_file):
    """
    Update the network settings.

    Example:
        $ sungazer network update-network-settings --config-file network_settings.json

    Example network_settings.json:
        {
          "lan2PortMode": "wan",
          "lan1IpAddress": "192.168.1.1",
          "lan1Netmask": "255.255.255.0",
          "lan1dhcpRange": "192.168.1.100-192.168.1.200",
          "dhcpStatus": "enabled"
        }

    """
    client = ctx.obj["client"]

    # Load from file
    config_data = read_json_file(config_file)
    config = GeneralSettings(**config_data)

    result = client.network.update_network_settings(config)
    output_formatter(result.model_dump(), ctx.obj["output_format"])


@network.command(name="get-interfaces")
@click.pass_context
@handle_exceptions
def get_interfaces(ctx):
    """
    Get the list of network interfaces.

    Example:
        $ sungazer network get-interfaces

    """
    client = ctx.obj["client"]
    result = client.network.get_interfaces()
    output_formatter(result.model_dump(), ctx.obj["output_format"])


@network.command(name="get-pingable-devices")
@click.pass_context
@handle_exceptions
def get_pingable_devices(ctx):
    """
    Get the list of pingable devices from devices.lua.

    Example:
        $ sungazer network get-pingable-devices

    """
    client = ctx.obj["client"]
    result = client.network.get_pingable_devices()
    output_formatter(result.model_dump(), ctx.obj["output_format"])
