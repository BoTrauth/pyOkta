"""Bulk cleanup operations."""


async def cleanup_all(client, skip_apps: bool = False, skip_groups: bool = False, skip_users: bool = False):
    """
    Clean up all Okta resources (users, groups, applications).

    Args:
        client: OktaClientWrapper instance.
        skip_apps: Skip application cleanup.
        skip_groups: Skip group cleanup.
        skip_users: Skip user cleanup.
    """
    from . import app_operations, group_operations, user_operations

    print("=" * 60)
    print("OKTA CLEANUP - WARNING: This will delete resources!")
    print("=" * 60)

    # Cleanup applications
    if not skip_apps:
        print("\n=== Cleaning up Applications ===")
        apps = await client.get_all_applications()
        for app in apps:
            if client.is_protected_app(app.id):
                print(f"SKIPPED: Protected application {getattr(app, 'label', 'unknown')} (ID: {app.id})")
                continue

            app_label = getattr(app, "label", "unknown")
            print(f"Deleting application: {app_label} (ID: {app.id})")
            # Deactivate first
            _, err = await client.client.deactivate_application(app.id)
            if err and "E0000007" not in str(err):
                print(f"  ⚠️  Could not deactivate, attempting delete anyway...")
            # Now delete
            await app_operations.delete_application(client, app.id, deactivate_first=False)

    # Cleanup groups
    if not skip_groups:
        print("\n=== Cleaning up Groups ===")
        groups = await client.get_all_groups()
        for group in groups:
            if client.is_protected_group(group.id):
                group_name = getattr(group.profile, "name", "unknown") if hasattr(group, "profile") else "unknown"
                print(f"SKIPPED: Protected group {group_name} (ID: {group.id})")
                continue

            group_name = getattr(group.profile, "name", "unknown") if hasattr(group, "profile") else "unknown"
            print(f"Deleting group: {group_name} (ID: {group.id})")
            await group_operations.delete_group(client, group.id)

    # Cleanup users
    if not skip_users:
        print("\n=== Cleaning up Users ===")
        users = await client.get_all_users()
        for user in users:
            if client.is_protected_user(user):
                user_login = getattr(user.profile, "login", "unknown")
                print(f"SKIPPED: Protected user {user_login} (ID: {user.id})")
                continue

            user_login = getattr(user.profile, "login", "unknown")
            print(f"Processing user: {user_login} (ID: {user.id})")

            # Deactivate if active
            if user.status == "ACTIVE":
                print(f"  Deactivating user {user_login}...")
                await user_operations.deactivate_user(client, user.id)

            # Delete user
            print(f"  Deleting user {user_login}...")
            await user_operations.delete_user(client, user.id)

    print("\n" + "=" * 60)
    print("Cleanup completed!")
    print("=" * 60)
