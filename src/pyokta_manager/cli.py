"""Command-line interface for PyOkta Manager."""

import asyncio
import functools
import sys
from pathlib import Path

import click

from .client import OktaClientWrapper
from .config import OktaConfig


def async_command(f):
    """Decorator to run async click commands."""

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper


@click.group()
@click.option("--env-file", type=click.Path(exists=True), help="Path to .env file")
@click.option("--env", type=click.Choice(['dev', 'qa', 'prev'], case_sensitive=False), help="Environment to use (dev, qa, or prev)")
@click.pass_context
def cli(ctx, env_file, env):
    """PyOkta Manager - Okta user, group, and application management tool."""
    try:
        config = OktaConfig(env_file, environment=env)
        ctx.obj = OktaClientWrapper(config)
    except ValueError as e:
        click.echo(f"❌ Configuration error: {e}", err=True)
        sys.exit(1)


# ==================== USER COMMANDS ====================


@cli.group()
def users():
    """User management commands."""
    pass


@users.command("list")
@click.option("--status", help="Filter by status (ACTIVE, DEPROVISIONED, etc.)")
@click.option("--output", "-o", help="Save output to JSON file")
@click.pass_obj
@async_command
async def users_list(client, status, output):
    """List all users."""
    from .user_operations import list_users

    await list_users(client, status=status, output_file=output)


@users.command("export")
@click.option("--output-dir", "-o", default="Output", help="Output directory")
@click.pass_obj
@async_command
async def users_export(client, output_dir):
    """Export users by status to separate JSON files."""
    from .user_operations import export_users_by_status

    await export_users_by_status(client, output_dir=output_dir)


@users.command("create")
@click.option("--first-name", "-f", required=True, help="First name")
@click.option("--last-name", "-l", required=True, help="Last name")
@click.option("--email", "-e", required=True, help="Email address")
@click.option("--password", "-p", help="Password")
@click.option("--activate", is_flag=True, help="Activate user immediately")
@click.pass_obj
@async_command
async def users_create(client, first_name, last_name, email, password, activate):
    """Create a new user."""
    from .user_operations import create_user

    await create_user(client, first_name, last_name, email, password, activate)


@users.command("activate")
@click.argument("user_id")
@click.option("--send-email/--no-send-email", default=True, help="Send activation email")
@click.pass_obj
@async_command
async def users_activate(client, user_id, send_email):
    """Activate a user."""
    from .user_operations import activate_user

    await activate_user(client, user_id, send_email)


@users.command("deactivate")
@click.argument("user_id")
@click.pass_obj
@async_command
async def users_deactivate(client, user_id):
    """Deactivate a user."""
    from .user_operations import deactivate_user

    await deactivate_user(client, user_id)


@users.command("delete")
@click.argument("user_id")
@click.confirmation_option(prompt="Are you sure you want to delete this user?")
@click.pass_obj
@async_command
async def users_delete(client, user_id):
    """Delete a user."""
    from .user_operations import delete_user

    await delete_user(client, user_id)


@users.command("delete-deprovisioned")
@click.option("--log-dir", default="Logs", help="Log directory")
@click.confirmation_option(prompt="Are you sure you want to delete all deprovisioned users?")
@click.pass_obj
@async_command
async def users_delete_deprovisioned(client, log_dir):
    """Delete all deprovisioned users."""
    from .user_operations import delete_deprovisioned_users

    await delete_deprovisioned_users(client, log_dir)


@users.command("delete-all")
@click.option("--log-dir", default="Logs", help="Log directory")
@click.confirmation_option(prompt="⚠️  WARNING: This will DELETE ALL USERS except protected ones. Are you absolutely sure?")
@click.pass_obj
@async_command
async def users_delete_all(client, log_dir):
    """Delete all users (deactivates first if needed), except protected users."""
    from .user_operations import delete_all_users

    await delete_all_users(client, log_dir)


# ==================== GROUP COMMANDS ====================


@cli.group()
def groups():
    """Group management commands."""
    pass


@groups.command("list")
@click.option("--output", "-o", help="Save output to JSON file")
@click.pass_obj
@async_command
async def groups_list(client, output):
    """List all groups."""
    from .group_operations import list_groups

    await list_groups(client, output_file=output)


@groups.command("create")
@click.option("--name", "-n", required=True, help="Group name")
@click.option("--description", "-d", default="", help="Group description")
@click.pass_obj
@async_command
async def groups_create(client, name, description):
    """Create a new group."""
    from .group_operations import create_group

    await create_group(client, name, description)


@groups.command("delete")
@click.argument("group_id")
@click.confirmation_option(prompt="Are you sure you want to delete this group?")
@click.pass_obj
@async_command
async def groups_delete(client, group_id):
    """Delete a group."""
    from .group_operations import delete_group

    await delete_group(client, group_id)


@groups.command("delete-all")
@click.option("--log-dir", default="Logs", help="Log directory")
@click.confirmation_option(prompt="⚠️  WARNING: This will DELETE ALL GROUPS except protected ones. Are you absolutely sure?")
@click.pass_obj
@async_command
async def groups_delete_all(client, log_dir):
    """Delete all groups except protected groups."""
    from .group_operations import delete_all_groups

    await delete_all_groups(client, log_dir)


@groups.command("add-user")
@click.argument("group_id")
@click.argument("user_id")
@click.pass_obj
@async_command
async def groups_add_user(client, group_id, user_id):
    """Add a user to a group."""
    from .group_operations import add_user_to_group

    await add_user_to_group(client, group_id, user_id)


@groups.command("remove-user")
@click.argument("group_id")
@click.argument("user_id")
@click.pass_obj
@async_command
async def groups_remove_user(client, group_id, user_id):
    """Remove a user from a group."""
    from .group_operations import remove_user_from_group

    await remove_user_from_group(client, group_id, user_id)


# ==================== APPLICATION COMMANDS ====================


@cli.group()
def apps():
    """Application management commands."""
    pass


@apps.command("list")
@click.option("--output", "-o", help="Save output to JSON file")
@click.pass_obj
@async_command
async def apps_list(client, output):
    """List all applications."""
    from .app_operations import list_applications

    await list_applications(client, output_file=output)


@apps.command("delete")
@click.argument("app_id")
@click.confirmation_option(prompt="Are you sure you want to delete this application?")
@click.pass_obj
@async_command
async def apps_delete(client, app_id):
    """Delete an application."""
    from .app_operations import delete_application

    await delete_application(client, app_id)


@apps.command("delete-all")
@click.option("--log-dir", default="Logs", help="Log directory")
@click.confirmation_option(prompt="⚠️  WARNING: This will DELETE ALL APPLICATIONS except protected ones. Are you absolutely sure?")
@click.pass_obj
@async_command
async def apps_delete_all(client, log_dir):
    """Delete all applications except protected applications."""
    from .app_operations import delete_all_applications

    await delete_all_applications(client, log_dir)


# ==================== LIST ALL COMMAND ====================


@cli.command("list-all")
@click.option("--output-dir", "-o", help="Save outputs to directory (creates separate files for users, groups, apps)")
@click.pass_obj
@async_command
async def list_all(client, output_dir):
    """List all users, groups, and applications."""
    from .user_operations import list_users
    from .group_operations import list_groups
    from .app_operations import list_applications

    users_output = f"{output_dir}/users.json" if output_dir else None
    await list_users(client, output_file=users_output)
    
    click.echo()
    groups_output = f"{output_dir}/groups.json" if output_dir else None
    await list_groups(client, output_file=groups_output)
    
    click.echo()
    apps_output = f"{output_dir}/apps.json" if output_dir else None
    await list_applications(client, output_file=apps_output)


# ==================== CLEANUP COMMANDS ====================


@cli.command("cleanup")
@click.option("--skip-apps", is_flag=True, help="Skip application cleanup")
@click.option("--skip-groups", is_flag=True, help="Skip group cleanup")
@click.option("--skip-users", is_flag=True, help="Skip user cleanup")
@click.confirmation_option(
    prompt="⚠️  WARNING: This will delete resources from Okta. Are you sure?"
)
@click.pass_obj
@async_command
async def cleanup(client, skip_apps, skip_groups, skip_users):
    """Clean up all Okta resources (with protection for specified IDs)."""
    from .cleanup_operations import cleanup_all

    await cleanup_all(client, skip_apps, skip_groups, skip_users)


def main():
    """Entry point for the CLI."""
    cli()


if __name__ == "__main__":
    main()
