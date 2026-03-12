"""User management operations."""

import json
from pathlib import Path
from typing import List, Optional


async def list_users(client, status: Optional[str] = None, output_file: Optional[str] = None):
    """
    List all users, optionally filtered by status.

    Args:
        client: OktaClientWrapper instance.
        status: Optional user status filter (ACTIVE, DEPROVISIONED, etc.).
        output_file: Optional file path to save JSON output.

    Returns:
        List of users.
    """
    # By default, Okta API only returns ACTIVE users. We need to explicitly request all statuses.
    if status:
        query_params = {"filter": f'status eq "{status}"'}
    else:
        # Request all users regardless of status
        query_params = {"search": 'status pr'}

    users = await client.get_all_users(query_params=query_params)

    print(f"Found {len(users)} users" + (f" with status {status}" if status else ""))
    print()
    
    # Print user list
    for user in users:
        name = f"{getattr(user.profile, 'firstName', '')} {getattr(user.profile, 'lastName', '')}".strip()
        user_id = user.id
        status_str = user.status
        email = user.profile.email
        print(f"  {name:<30} {user_id:<25} {status_str:<20} {email}")

    if output_file:
        # Convert users to serializable format
        users_data = [
            {
                "id": u.id,
                "status": u.status,
                "created": str(u.created),
                "activated": str(u.activated) if u.activated else None,
                "statusChanged": str(u.status_changed) if u.status_changed else None,
                "lastLogin": str(u.last_login) if u.last_login else None,
                "profile": {
                    "login": u.profile.login,
                    "email": u.profile.email,
                    "firstName": getattr(u.profile, "firstName", ""),
                    "lastName": getattr(u.profile, "lastName", ""),
                },
            }
            for u in users
        ]

        Path(output_file).parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, "w") as f:
            json.dump(users_data, f, indent=2)
        print(f"Saved to {output_file}")

    return users


async def export_users_by_status(client, output_dir: str = "Output"):
    """
    Export users grouped by status into separate JSON files.

    Args:
        client: OktaClientWrapper instance.
        output_dir: Directory to save output files.
    """
    statuses = [
        "STAGED",
        "PROVISIONED",
        "ACTIVE",
        "RECOVERY",
        "PASSWORD_EXPIRED",
        "LOCKED_OUT",
        "SUSPENDED",
        "DEPROVISIONED",
    ]

    for status in statuses:
        output_file = f"{output_dir}/okta_users_{status}.json"
        users = await list_users(client, status=status, output_file=output_file)
        print(f"{status}: {len(users)} users")


async def activate_user(client, user_id: str, send_email: bool = True):
    """
    Activate a user.

    Args:
        client: OktaClientWrapper instance.
        user_id: User ID to activate.
        send_email: Whether to send activation email.

    Returns:
        Activated user object or None on error.
    """
    res, resp, err = await client.client.activate_user(
        user_id, query_params={"sendEmail": str(send_email).lower()}
    )
    if err:
        print(f"❌ Failed to activate {user_id}: {err}")
        return None

    print(f"✅ User {user_id} activated successfully")
    return res


async def deactivate_user(client, user_id: str):
    """
    Deactivate a user.

    Args:
        client: OktaClientWrapper instance.
        user_id: User ID to deactivate.

    Returns:
        Response or None on error.
    """
    res, err = await client.client.deactivate_user(user_id)
    if err:
        print(f"❌ Failed to deactivate {user_id}: {err}")
        return None

    print(f"✅ User {user_id} deactivated successfully")
    return res


async def delete_user(client, user_id: str):
    """
    Delete a user (must be deactivated first).

    Args:
        client: OktaClientWrapper instance.
        user_id: User ID to delete.

    Returns:
        True if successful, False otherwise.
    """
    _, err = await client.client.deactivate_or_delete_user(user_id)
    if err:
        print(f"❌ Failed to delete user {user_id}: {err}")
        return False

    print(f"✅ User {user_id} deleted successfully")
    return True


async def create_user(
    client,
    first_name: str,
    last_name: str,
    email: str,
    password: Optional[str] = None,
    activate: bool = False,
):
    """
    Create a new user.

    Args:
        client: OktaClientWrapper instance.
        first_name: User's first name.
        last_name: User's last name.
        email: User's email (used as login).
        password: Optional password.
        activate: Whether to activate user immediately.

    Returns:
        Created user object or None on error.
    """
    user_profile = {
        "firstName": first_name,
        "lastName": last_name,
        "email": email,
        "login": email,
    }

    credentials = None
    if password:
        credentials = {"password": {"value": password}}

    create_user_request = {
        "profile": user_profile,
        "credentials": credentials,
    }

    query_params = {"activate": str(activate).lower()}

    user, resp, err = await client.client.create_user(create_user_request, query_params)
    if err:
        print(f"❌ Failed to create user {email}: {err}")
        return None

    print(f"✅ User {email} created successfully (ID: {user.id})")
    return user


async def delete_deprovisioned_users(client, log_dir: str = "Logs"):
    """
    Delete all deprovisioned users.

    Args:
        client: OktaClientWrapper instance.
        log_dir: Directory to save deletion logs.

    Returns:
        Tuple of (successful_count, failed_count).
    """
    import time

    users = await list_users(client, status="DEPROVISIONED")

    if not users:
        print("No deprovisioned users found.")
        return 0, 0

    # Create log file
    Path(log_dir).mkdir(parents=True, exist_ok=True)
    log_file = Path(log_dir) / f"deletion_log_{int(time.time())}.txt"

    successful = 0
    failed = 0

    with open(log_file, "w") as log:
        log.write(f"Deletion started at {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        log.write(f"Total users to delete: {len(users)}\n\n")

        for user in users:
            user_id = user.id
            user_login = getattr(user.profile, "login", "unknown")

            if client.is_protected_user(user):
                msg = f"SKIPPED: Protected user {user_login} (ID: {user_id})"
                print(msg)
                log.write(f"{msg}\n")
                continue

            try:
                _, err = await client.client.deactivate_or_delete_user(user_id)
                if err:
                    msg = f"ERROR: Failed to delete {user_login} (ID: {user_id}): {err}"
                    print(msg)
                    log.write(f"{msg}\n")
                    failed += 1
                else:
                    msg = f"SUCCESS: Deleted {user_login} (ID: {user_id})"
                    print(msg)
                    log.write(f"{msg}\n")
                    successful += 1
            except Exception as e:
                msg = f"EXCEPTION: Error deleting {user_login} (ID: {user_id}): {str(e)}"
                print(msg)
                log.write(f"{msg}\n")
                failed += 1

        log.write(f"\n\nDeletion completed at {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        log.write(f"Successful: {successful}\n")
        log.write(f"Failed: {failed}\n")

    print(f"\n📊 Summary: {successful} deleted, {failed} failed")
    print(f"📝 Log saved to {log_file}")

    return successful, failed


async def delete_all_users(client, log_dir: str = "Logs"):
    """
    Delete all users (deactivates first if needed), except protected users.

    Args:
        client: OktaClientWrapper instance.
        log_dir: Directory to save deletion logs.

    Returns:
        Tuple of (successful_count, failed_count, skipped_count).
    """
    import time

    # Get all users regardless of status - use search parameter to include all statuses
    users = await client.get_all_users(query_params={"search": "status pr"})

    if not users:
        print("No users found.")
        return 0, 0, 0

    # Create log file
    Path(log_dir).mkdir(parents=True, exist_ok=True)
    log_file = Path(log_dir) / f"delete_all_log_{int(time.time())}.txt"

    successful = 0
    failed = 0
    skipped = 0

    with open(log_file, "w") as log:
        log.write(f"Delete all users started at {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        log.write(f"Total users to process: {len(users)}\n\n")

        for user in users:
            user_id = user.id
            user_login = getattr(user.profile, "login", "unknown")
            user_status = user.status

            if client.is_protected_user(user):
                msg = f"PROTECTED: Skipped {user_login} (ID: {user_id}, Status: {user_status})"
                print(msg)
                log.write(f"{msg}\n")
                skipped += 1
                continue

            try:
                # Deactivate first if not already deprovisioned
                if user_status != "DEPROVISIONED":
                    _, err = await client.client.deactivate_user(user_id)
                    if err:
                        msg = f"ERROR: Failed to deactivate {user_login} (ID: {user_id}): {err}"
                        print(msg)
                        log.write(f"{msg}\n")
                        failed += 1
                        continue
                    print(f"  Deactivated {user_login}")
                    log.write(f"  Deactivated {user_login} (ID: {user_id})\n")

                # Now delete
                _, err = await client.client.deactivate_or_delete_user(user_id)
                if err:
                    msg = f"ERROR: Failed to delete {user_login} (ID: {user_id}): {err}"
                    print(msg)
                    log.write(f"{msg}\n")
                    failed += 1
                else:
                    msg = f"SUCCESS: Deleted {user_login} (ID: {user_id}, was {user_status})"
                    print(msg)
                    log.write(f"{msg}\n")
                    successful += 1
            except Exception as e:
                msg = f"EXCEPTION: Error processing {user_login} (ID: {user_id}): {str(e)}"
                print(msg)
                log.write(f"{msg}\n")
                failed += 1

        log.write(f"\n\nDeletion completed at {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        log.write(f"Successful: {successful}\n")
        log.write(f"Failed: {failed}\n")
        log.write(f"Skipped (Protected): {skipped}\n")

    print(f"\n📊 Summary: {successful} deleted, {failed} failed, {skipped} protected/skipped")
    print(f"📝 Log saved to {log_file}")

    return successful, failed, skipped
