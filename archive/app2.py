import asyncio
import logging
from okta.client import Client as OktaClient

DAVES_EMAIL = "dave.brann@intergraph.com";
LST_APPLICATIONS_IDs_NOT_TO_DELETE = ["0oa21xdyzhwikdX280h8", "0oa22tx82jcE9a4wT0h8", "0oa25xglftsc8nNHv0h8", "0oa26qqqk43cdHche0h8",
                                "0oaa8odrx5HNseYOL0h7", "0oawg28lf8wcmkrD50h7", "0oawhtx8rjdYqDl4p0h7"]
LST_GROUPS_IDS_NOT_TO_DELETE = ['00ga8odrxaV0HtAb90h7', '00g1m0nlnaby0URcX0h8']

async def get_all_users(client):
    """Retrieve all users using built-in pagination."""
    all_users = []
    # Get the first page of users.
    users, resp, err = await client.list_users()
    if err:
        print("Error fetching users:", err)
        return all_users

    # Add the first page to our list.
    all_users.extend(users)
    # Continue retrieving pages while available.
    while resp.has_next():
        users, err = await resp.next()
        if err:
            print("Error fetching next page:", err)
            break
        all_users.extend(users)
    return all_users

async def get_all_groups(client):
    """Retrieve all groups using built-in pagination."""
    all_groups = []
    groups, resp, err = await client.list_groups()
    if err:
        print("Error listing groups:", err)
        return all_groups
    all_groups.extend(groups)
    while resp.has_next():
        groups, err = await resp.next()
        if err:
            print("Error fetching next page of groups:", err)
            break
        all_groups.extend(groups)
    return all_groups

# ---------- Application Cleanup ----------
# For each application, list all assigned users (via a direct API call)
# and remove each assignment.
async def cleanup_applications(client):
    print("=== Cleaning up Applications ===")
    apps, resp, err = await client.list_applications()
    if err:
        print("Error listing applications:", err)
        return

    for app in apps:
        if app.id not in LST_APPLICATIONS_IDs_NOT_TO_DELETE:
            app_id = app.id
            app_label = getattr(app, "label", "unknown")
            print(f"Deleting application: {app_label} (ID: {app_id})")
            # Call the SDK method to delete the application.
            _, del_err = await client.delete_application(app_id)
            if del_err:
                print(f"Error deleting application {app_label}: {del_err}")
            else:
                print(f"Application {app_label} deleted successfully.")

# ---------- Group Cleanup ----------
# For each group, list its members (using a GET to the groups endpoint),
# remove each member using the SDK function, and then delete the group.
async def cleanup_groups(client):
    """Delete all groups from the Okta org."""
    print("=== Deleting Groups ===")
    groups = await get_all_groups(client)
    for group in groups:
        if group.id not in LST_GROUPS_IDS_NOT_TO_DELETE:
            group_id = group.id
            # Attempt to read group name; fallback to "unknown" if unavailable.
            group_name = getattr(group.profile, "name", "unknown") if hasattr(group, "profile") else "unknown"
            print(f"Deleting group: {group_name} (ID: {group_id})")
            # Call the SDK method to delete the group.
            _, del_err = await client.delete_group(group_id)
            if del_err:
                print(f"Error deleting group '{group_name}': {del_err}")
            else:
                print(f"Group '{group_name}' deleted successfully.")

# ---------- User Cleanup ----------
# For each user, if active then first deactivate (if needed) and then delete.
async def cleanup_users(client):
    print("\n=== Cleaning up Users ===")

    users = await get_all_users(client)

    for user in users:
        user_id = user.id
        user_login = user.profile.login if hasattr(user.profile, "login") else "unknown"
        if user.profile.login != DAVES_EMAIL and user.profile.email != DAVES_EMAIL:
            print(f"\nProcessing User: {user_login} (ID: {user_id})")
            try:
                # If the user is active, deactivate them first.
                if user.status == "ACTIVE":
                    print(f"  Deactivating user {user_login} ...")
                    _, deact_err = await client.deactivate_or_delete_user(user_id)
                    if deact_err:
                        print(f"    Error deactivating user {user_login}: {deact_err}")
                    else:
                        print(f"    User {user_login} deactivated.")
                # Now delete the user.
                print(f"  Deleting user {user_login} ...")
                _, del_err = await client.deactivate_or_delete_user(user_id)
                if del_err:
                    print(f"    Error deleting user {user_login}: {del_err}")
                else:
                    print(f"    User {user_login} deleted.")
            except Exception as e:
                print(f"  Exception processing user {user_login}: {e}")

# ---------- Main Function ----------
async def main():
    # Updated configuration using OAuth 2.0 with a private key.
    config = {
        'orgUrl': 'https://dev-520699.oktapreview.com',   # Your Okta domain
        "authorizationMode": "PrivateKey",
        'clientId': '0oa25xglftsc8nNHv0h8',
        "scopes": ["okta.users.manage", "okta.groups.manage", "okta.apps.manage"],
        "privateKey": "{\"d\": \"FfWD0vuFUTHkJxVmgO4u0ZrGqTO_76_YNB_nC3BLCLOXzzjO65ytU5H_BgcTzL-2lvekNTqHMzBpnr5cSidugqoCV4i5ah62hmazOi6mRl6mmhLpptj9cTenwzbQhUhFK20cdOfdnuJspUo7d7_hzGodobUrVBzJIcs3ml3wFtMBeld6BSD8jIQhHp0nrHAOP2I6lkgC4OL5JzVYWFFY7A_f_HBPm-QXLjHLpQ0_hq2rDy7hADwknV5VBYz5GebU0ps1IFDgVfSwRqyaMG-SUGUafXYxrKhoTb1AylN0yQ6gGj4mQDRNveSY_j5YmEGXqmY9zgfctDAfQBYp1im7IQ\", \"p\": \"4N2uOWm3-d8CNg4p-OA_zY_pw2_6SrS0qMZj4X2o4ukGDLU2wPtNeMBzVyiOfkGsiSuBl_dfTKJZobEV4upIq3ytHWnkAu-7VcyIm7_01s402tpoXNMt51JAsnnJ6PYIKr6uUcLySCSontWelwG594mCW4ACwkYPBpgk6C62amE\", \"q\": \"x1jsRXLA6swWnFp9hwHBXYVUAoeCwNjjG1dFpsP6jUQX1aRaZpTCD3oYU0FsItMnxzWc40s-mYfV-YhElXkBZNyWza4UtwUwoyFf7gHjWh8dwrfX2Zhe1vvJYuJWJ7tWBz_XyMeaJIUQ3CDavXw5oshRV_3Rj6vbSx2Uo0YXWqU\", \"dp\": \"TH1751G74EZoxSR6SItXiMA8f1uW41Sm44ZgsXKCQXWMtkPqNSkGyF2Gno5QMkh6vUpMUfo2s6XCIYtQa5jQUW0eohPEGO-dZOknSvu3-F26gvuqZnD7e2VyVoOxGAqg6pFkULGkor-9kBIQWUOgE8D109QunBEiyVZ1r3k8WeE\", \"dq\": \"PhKzZ6Cm77XjKIaI5dwnEO7uTOdTUKd4eFABkT8fKpPUdCL8P0r87oLPRkVt3Z4wmbhZBPGuKXKBr3S-HmkShQynLJ6TNrY4AePnkh4mZC6iPrquTMREa971Q4RE3ZRY4mL_1zZICi0hJdpZIn2nGMgVhDe15G3YGBi66uhtZz0\", \"qi\": \"hnVclED8kBMm83RFVi8hYEF2JhNo2ATBImlDovxjkWHrDkNuk8lkADIJKONwLHQSZ0z0UHZAkzHlVOZ2oMqaHZa9t_nsEd5MC1_5YuvYlhcFYof29Rodmtcn4zRUn2bQ0Tj-NvUazS6iGvwcKQi7SHMq4yYZvEiaeHUmWBR5J50\", \"kty\": \"RSA\", \"e\": \"AQAB\", \"kid\": \"o9jT-aVK-SswdaqpwwY-jFgavJGEsnIJfCMd6qPEf_A\", \"n\": \"rxpuK-ITaX96N6HrV-oAYfrabTv4-V3KuErK1SyAlHjnBWZtg9CXI6LKqsYND7D8wieMV6Sf0CTnn6BoLQgghZR96xYDMBbSFUv_f3pzS8YQNEBv8IIVk59gnDIMCrVf_1LP1mVbe4cZTo9aOm30eAL93l6FRtexpiHq0mB3Ap47vg7mcrlYNoew0K68ImEwTGV6ip7WlQ5XUBFh3wdohslNcI5QUZtV7t67sFD5hk8Bt6-fZ1BfxKAUUy7WE_fU4nl2MeEW7dwSE8nmRs8ggMiv82h326mtzwC7afJ7sAiY04IT2veinDOADPNBRtUtIQm980N85Go2Tk1PUa-qhQ\"}",
        # "kid": "your_key_id_here"
    }
    client = OktaClient(config)
    
    # (Optional) Enable logging for more detail.
    logging.basicConfig(level=logging.INFO)

    # Run cleanup steps in order.
    await cleanup_applications(client)
    await cleanup_groups(client)
    await cleanup_users(client)


if __name__ == "__main__":
    asyncio.run(main())
