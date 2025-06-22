import click

from sungazer.cli.main import handle_exceptions, output_formatter


@click.group(name="certificate")
def certificate():
    """Certificate operations."""


@certificate.command(name="renew-mqtt")
@click.pass_context
@handle_exceptions
def renew_mqtt(ctx):
    """
    Renew the MQTT certificate.

    Runs /usr/local/sbin/cert_client.sh MQTT under the hood and confirms with
    /usr/local/sbin/cert_check.sh if the cert is valid.

    Example:
        $ sungazer certificate renew-mqtt

    """
    client = ctx.obj["client"]
    result = client.certificates.renew_mqtt()
    output_formatter(result.model_dump(), ctx.obj["output_format"])
