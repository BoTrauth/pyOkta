"""Group management operations."""

from typing import Optional


async def list_groups(client, output_file: Optional[str] = None):
    """
    List all groups.

    Args:
        client: OktaClientWrapper instance.
        output_file: Optional file path to save JSON output.

    Returns:
        List of groups.
    """
    groups = await client.get_all_groups()
    print(f"Found {len(groups)} groups")
    print()

    for group in groups:
        group_name = getattr(group.profile, "name", "unknown") if hasattr(group, "profile") else "unknown"
        group_desc = getattr(group.profile, "description", "") if hasattr(group, "profile") else ""
        print(f"  {group_name:<40} {group.id:<25} {group_desc}")

    if output_file:
        import json
        from pathlib import Path

        groups_data = [
            {
                "id": g.id,
                "created": str(g.created),
                "lastUpdated": str(g.last_updated),
                "lastMembershipUpdated": str(g.last_membership_updated) if hasattr(g, "last_membership_updated") else None,
                "type": g.type,
                "profile": {
                    "name": getattr(g.profile, "name", "") if hasattr(g, "profile") else "",
                    "description": getattr(g.profile, "description", "") if hasattr(g, "profile") else "",
                },
            }
            for g in groups
        ]

        Path(output_file).parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, "w") as f:
            json.dump(groups_data, f, indent=2)
        print(f"Saved to {output_file}")

    return groups


async def create_group(client, name: str, description: str = ""):
    """
    Create a new group.

    Args:
        client: OktaClientWrapper instance.
        name: Group name.
        description: Group description.

    Returns:
        Created group object or None on error.
    """
    group_profile = {
        "name": name,
        "description": description,
    }

    group, resp, err = await client.client.create_group({"profile": group_profile})
    if err:
        print(f"❌ Failed to create group {name}: {err}")
        return None

    print(f"✅ Group {name} created successfully (ID: {group.id})")
    return group


async def delete_group(client, group_id: str):
    """
    Delete a group.

    Args:
        client: OktaClientWrapper instance.
        group_id: Group ID to delete.

    Returns:
        True if successful, False otherwise.
    """
    _, err = await client.client.delete_group(group_id)
    if err:
        print(f"❌ Failed to delete group {group_id}: {err}")
        return False

    print(f"✅ Group {group_id} deleted successfully")
    return True


async def add_user_to_group(client, group_id: str, user_id: str):
    """
    Add a user to a group.

    Args:
        client: OktaClientWrapper instance.
        group_id: Group ID.
        user_id: User ID.

    Returns:
        True if successful, False otherwise.
    """
    _, err = await client.client.add_user_to_group(group_id, user_id)
    if err:
        print(f"❌ Failed to add user {user_id} to group {group_id}: {err}")
        return False

    print(f"✅ User {user_id} added to group {group_id}")
    return True


async def remove_user_from_group(client, group_id: str, user_id: str):
    """
    Remove a user from a group.

    Args:
        client: OktaClientWrapper instance.
        group_id: Group ID.
        user_id: User ID.

    Returns:
        True if successful, False otherwise.
    """
    _, err = await client.client.remove_user_from_group(group_id, user_id)
    if err:
        print(f"❌ Failed to remove user {user_id} from group {group_id}: {err}")
        return False

    print(f"✅ User {user_id} removed from group {group_id}")
    return True


async def delete_all_groups(client, log_dir: str = "Logs"):
    """
    Delete all groups except protected groups.

    Args:
        client: OktaClientWrapper instance.
        log_dir: Directory to save deletion logs.

    Returns:
        Tuple of (successful_count, failed_count, skipped_count).
    """
    import time
    from pathlib import Path

    groups = await client.get_all_groups()

    if not groups:
        print("No groups found.")
        return 0, 0, 0

    # Create log file
    Path(log_dir).mkdir(parents=True, exist_ok=True)
    log_file = Path(log_dir) / f"delete_all_groups_log_{int(time.time())}.txt"

    successful = 0
    failed = 0
    skipped = 0

    with open(log_file, "w") as log:
        log.write(f"Delete all groups started at {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        log.write(f"Total groups to process: {len(groups)}\n\n")

        for group in groups:
            group_id = group.id
            group_name = getattr(group.profile, "name", "unknown") if hasattr(group, "profile") else "unknown"

            if client.is_protected_group(group_id):
                msg = f"PROTECTED: Skipped {group_name} (ID: {group_id})"
                print(msg)
                log.write(f"{msg}\n")
                skipped += 1
                continue

            try:
                _, err = await client.client.delete_group(group_id)
                if err:
                    msg = f"ERROR: Failed to delete {group_name} (ID: {group_id}): {err}"
                    print(msg)
                    log.write(f"{msg}\n")
                    failed += 1
                else:
                    msg = f"SUCCESS: Deleted {group_name} (ID: {group_id})"
                    print(msg)
                    log.write(f"{msg}\n")
                    successful += 1
            except Exception as e:
                msg = f"EXCEPTION: Error deleting {group_name} (ID: {group_id}): {str(e)}"
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
