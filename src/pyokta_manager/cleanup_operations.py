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
    print("🧹 OKTA CLEANUP - WARNING: This will delete resources!")
    print("=" * 60)

    # Track statistics
    apps_deleted = 0
    apps_failed = 0
    apps_skipped = 0
    
    groups_deleted = 0
    groups_failed = 0
    groups_skipped = 0
    
    users_deleted = 0
    users_failed = 0
    users_skipped = 0

    # Cleanup applications
    if not skip_apps:
        print("\n🔧 === Cleaning up Applications ===")
        apps = await client.get_all_applications()
        for app in apps:
            if client.is_protected_app(app.id):
                app_label = getattr(app, 'label', 'unknown')
                print(f"🛡️  PROTECTED: Skipped {app_label} (ID: {app.id})")
                apps_skipped += 1
                continue

            app_label = getattr(app, "label", "unknown")
            
            # Deactivate first
            _, err = await client.client.deactivate_application(app.id)
            if err and "E0000007" not in str(err):
                print(f"⏸️  Deactivating {app_label} (ID: {app.id})")
                print(f"  ⚠️  Could not deactivate, attempting delete anyway...")
            elif not err:
                print(f"⏸️  Deactivating {app_label} (ID: {app.id})")
            
            # Now delete
            print(f"🗑️  Deleting application: {app_label} (ID: {app.id})")
            _, err = await client.client.delete_application(app.id)
            if err:
                print(f"  ❌ ERROR: Failed to delete {app_label}: {err}")
                apps_failed += 1
            else:
                print(f"  ✅ SUCCESS: Deleted {app_label}")
                apps_deleted += 1

    # Cleanup groups
    if not skip_groups:
        print("\n👥 === Cleaning up Groups ===")
        groups = await client.get_all_groups()
        for group in groups:
            if client.is_protected_group(group.id):
                group_name = getattr(group.profile, "name", "unknown") if hasattr(group, "profile") else "unknown"
                print(f"🛡️  PROTECTED: Skipped {group_name} (ID: {group.id})")
                groups_skipped += 1
                continue

            group_name = getattr(group.profile, "name", "unknown") if hasattr(group, "profile") else "unknown"
            print(f"🗑️  Deleting group: {group_name} (ID: {group.id})")
            
            _, err = await client.client.delete_group(group.id)
            if err:
                print(f"  ❌ ERROR: Failed to delete {group_name}: {err}")
                groups_failed += 1
            else:
                print(f"  ✅ SUCCESS: Deleted {group_name}")
                groups_deleted += 1

    # Cleanup users
    if not skip_users:
        print("\n👤 === Cleaning up Users ===")
        users = await client.get_all_users(query_params={"search": "status pr"})
        for user in users:
            if client.is_protected_user(user):
                user_login = getattr(user.profile, "login", "unknown")
                print(f"🛡️  PROTECTED: Skipped {user_login} (ID: {user.id})")
                users_skipped += 1
                continue

            user_login = getattr(user.profile, "login", "unknown")

            # Deactivate if active
            if user.status == "ACTIVE":
                print(f"⏸️  Deactivating {user_login} (ID: {user.id})")
                _, err = await client.client.deactivate_user(user.id)
                if err:
                    print(f"  ❌ ERROR: Failed to deactivate {user_login}: {err}")
                    users_failed += 1
                    continue

            # Delete user
            print(f"🗑️  Deleting user: {user_login} (ID: {user.id})")
            _, err = await client.client.deactivate_or_delete_user(user.id)
            if err:
                print(f"  ❌ ERROR: Failed to delete {user_login}: {err}")
                users_failed += 1
            else:
                print(f"  ✅ SUCCESS: Deleted {user_login}")
                users_deleted += 1

    print("\n" + "=" * 60)
    print("✨ Cleanup completed!")
    print("=" * 60)
    
    # Print summary
    if not skip_apps:
        print(f"\n📱 Applications: ✅ {apps_deleted} deleted, ❌ {apps_failed} failed, 🛡️  {apps_skipped} protected")
    if not skip_groups:
        print(f"👥 Groups:       ✅ {groups_deleted} deleted, ❌ {groups_failed} failed, 🛡️  {groups_skipped} protected")
    if not skip_users:
        print(f"👤 Users:        ✅ {users_deleted} deleted, ❌ {users_failed} failed, 🛡️  {users_skipped} protected")
