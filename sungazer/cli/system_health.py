import click

from sungazer.cli.main import handle_exceptions, output_formatter


@click.group(name="system-health")
def system_health():
    """System health operations."""


@system_health.command(name="get-checklist")
@click.option(
    "--category",
    type=click.Choice(["ALL", "ACPV", "PLATFORM", "STORAGE"]),
    default="ALL",
    help="The category to get",
)
@click.pass_context
@handle_exceptions
def get_checklist(ctx, category):
    """
    Get the system health checklist.

    Example:
        $ sungazer system-health get-checklist --category ALL

    """
    client = ctx.obj["client"]
    result = client.system_health.get_checklist(category)
    output_formatter(result.model_dump(), ctx.obj["output_format"])


@system_health.command(name="start-check")
@click.option(
    "--check",
    required=True,
    multiple=True,
    help="Check to run (can be specified multiple times)",
)
@click.option(
    "--category",
    type=click.Choice(["ALL", "ACPV", "PLATFORM", "STORAGE"]),
    default="ALL",
    help="The category to check",
)
@click.pass_context
@handle_exceptions
def start_check(ctx, check: list[bool], category: str):
    """
    Start a system health check.

    Example:
        $ sungazer system-health start-check \
            --check network_ping \
            --check dns_resolution \
            --category PLATFORM

    """
    client = ctx.obj["client"]
    result = client.system_health.start_check(list(check), category)
    output_formatter(result.model_dump(), ctx.obj["output_format"])


@system_health.command(name="get-check-status")
@click.pass_context
@handle_exceptions
def get_check_status(ctx):
    """
    Get the system health check status.

    Example:
        $ sungazer system-health get-check-status

    """
    client = ctx.obj["client"]
    result = client.system_health.get_check_status()
    output_formatter([s.model_dump() for s in result], ctx.obj["output_format"])
