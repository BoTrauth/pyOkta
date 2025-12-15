"""Application management operations."""

from typing import Optional


async def list_applications(client, output_file: Optional[str] = None):
    """
    List all applications.

    Args:
        client: OktaClientWrapper instance.
        output_file: Optional file path to save JSON output.

    Returns:
        List of applications.
    """
    apps = await client.get_all_applications()
    print(f"Found {len(apps)} applications")
    print()

    for app in apps:
        app_label = getattr(app, "label", "unknown")
        app_status = getattr(app, "status", "UNKNOWN")
        print(f"  {app_label:<40} {app.id:<25} {app_status}")

    if output_file:
        import json
        from pathlib import Path

        apps_data = [
            {
                "id": a.id,
                "name": a.name,
                "label": getattr(a, "label", ""),
                "status": a.status,
                "created": str(a.created),
                "lastUpdated": str(a.last_updated),
            }
            for a in apps
        ]

        Path(output_file).parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, "w") as f:
            json.dump(apps_data, f, indent=2)
        print(f"Saved to {output_file}")

    return apps


async def delete_application(client, app_id: str, deactivate_first: bool = True):
    """
    Delete an application (deactivates first if needed).

    Args:
        client: OktaClientWrapper instance.
        app_id: Application ID to delete.
        deactivate_first: Whether to deactivate before deleting (default: True).

    Returns:
        True if successful, False otherwise.
    """
    # Deactivate first if requested
    if deactivate_first:
        _, err = await client.client.deactivate_application(app_id)
        if err:
            # Only print if it's not already inactive
            if "E0000007" not in str(err):  # Not found or already inactive
                print(f"  ⚠️  Note: Could not deactivate application {app_id}: {err}")
    
    # Now delete
    _, err = await client.client.delete_application(app_id)
    if err:
        print(f"❌ Failed to delete application {app_id}: {err}")
        return False

    print(f"✅ Application {app_id} deleted successfully")
    return True


async def delete_all_applications(client, log_dir: str = "Logs"):
    """
    Delete all applications except protected applications.

    Args:
        client: OktaClientWrapper instance.
        log_dir: Directory to save deletion logs.

    Returns:
        Tuple of (successful_count, failed_count, skipped_count).
    """
    import time
    from pathlib import Path

    apps = await client.get_all_applications()

    if not apps:
        print("No applications found.")
        return 0, 0, 0

    # Create log file
    Path(log_dir).mkdir(parents=True, exist_ok=True)
    log_file = Path(log_dir) / f"delete_all_apps_log_{int(time.time())}.txt"

    successful = 0
    failed = 0
    skipped = 0

    with open(log_file, "w") as log:
        log.write(f"Delete all applications started at {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        log.write(f"Total applications to process: {len(apps)}\n\n")

        for app in apps:
            app_id = app.id
            app_label = getattr(app, "label", "unknown")

            if client.is_protected_app(app_id):
                msg = f"PROTECTED: Skipped {app_label} (ID: {app_id})"
                print(msg)
                log.write(f"{msg}\n")
                skipped += 1
                continue

            try:
                # Deactivate first
                _, err = await client.client.deactivate_application(app_id)
                if err and "E0000007" not in str(err):
                    print(f"  ⚠️  Note: Could not deactivate {app_label}")
                    log.write(f"  Note: Could not deactivate {app_label} (ID: {app_id})\n")
                
                # Now delete
                _, err = await client.client.delete_application(app_id)
                if err:
                    msg = f"ERROR: Failed to delete {app_label} (ID: {app_id}): {err}"
                    print(msg)
                    log.write(f"{msg}\n")
                    failed += 1
                else:
                    msg = f"SUCCESS: Deleted {app_label} (ID: {app_id})"
                    print(msg)
                    log.write(f"{msg}\n")
                    successful += 1
            except Exception as e:
                msg = f"EXCEPTION: Error deleting {app_label} (ID: {app_id}): {str(e)}"
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
