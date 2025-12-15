import asyncio
import json
import time
import os
from okta.client import Client as OktaClient

# Reusing the same configuration from other scripts
config = {
    'orgUrl': 'https://dev-520699.oktapreview.com',
    'authorizationMode': 'PrivateKey',
    'clientId': '0oa25xglftsc8nNHv0h8',
    'scopes': [
        'okta.users.manage', 
        'okta.groups.manage', 
        'okta.apps.manage'
    ],
    'privateKey': "{\"d\": \"FfWD0vuFUTHkJxVmgO4u0ZrGqTO_76_YNB_nC3BLCLOXzzjO65ytU5H_BgcTzL-2lvekNTqHMzBpnr5cSidugqoCV4i5ah62hmazOi6mRl6mmhLpptj9cTenwzbQhUhFK20cdOfdnuJspUo7d7_hzGodobUrVBzJIcs3ml3wFtMBeld6BSD8jIQhHp0nrHAOP2I6lkgC4OL5JzVYWFFY7A_f_HBPm-QXLjHLpQ0_hq2rDy7hADwknV5VBYz5GebU0ps1IFDgVfSwRqyaMG-SUGUafXYxrKhoTb1AylN0yQ6gGj4mQDRNveSY_j5YmEGXqmY9zgfctDAfQBYp1im7IQ\", \"p\": \"4N2uOWm3-d8CNg4p-OA_zY_pw2_6SrS0qMZj4X2o4ukGDLU2wPtNeMBzVyiOfkGsiSuBl_dfTKJZobEV4upIq3ytHWnkAu-7VcyIm7_01s402tpoXNMt51JAsnnJ6PYIKr6uUcLySCSontWelwG594mCW4ACwkYPBpgk6C62amE\", \"q\": \"x1jsRXLA6swWnFp9hwHBXYVUAoeCwNjjG1dFpsP6jUQX1aRaZpTCD3oYU0FsItMnxzWc40s-mYfV-YhElXkBZNyWza4UtwUwoyFf7gHjWh8dwrfX2Zhe1vvJYuJWJ7tWBz_XyMeaJIUQ3CDavXw5oshRV_3Rj6vbSx2Uo0YXWqU\", \"dp\": \"TH1751G74EZoxSR6SItXiMA8f1uW41Sm44ZgsXKCQXWMtkPqNSkGyF2Gno5QMkh6vUpMUfo2s6XCIYtQa5jQUW0eohPEGO-dZOknSvu3-F26gvuqZnD7e2VyVoOxGAqg6pFkULGkor-9kBIQWUOgE8D109QunBEiyVZ1r3k8WeE\", \"dq\": \"PhKzZ6Cm77XjKIaI5dwnEO7uTOdTUKd4eFABkT8fKpPUdCL8P0r87oLPRkVt3Z4wmbhZBPGuKXKBr3S-HmkShQynLJ6TNrY4AePnkh4mZC6iPrquTMREa971Q4RE3ZRY4mL_1zZICi0hJdpZIn2nGMgVhDe15G3YGBi66uhtZz0\", \"qi\": \"hnVclED8kBMm83RFVi8hYEF2JhNo2ATBImlDovxjkWHrDkNuk8lkADIJKONwLHQSZ0z0UHZAkzHlVOZ2oMqaHZa9t_nsEd5MC1_5YuvYlhcFYof29Rodmtcn4zRUn2bQ0Tj-NvUazS6iGvwcKQi7SHMq4yYZvEiaeHUmWBR5J50\", \"kty\": \"RSA\", \"e\": \"AQAB\", \"kid\": \"o9jT-aVK-SswdaqpwwY-jFgavJGEsnIJfCMd6qPEf_A\", \"n\": \"rxpuK-ITaX96N6HrV-oAYfrabTv4-V3KuErK1SyAlHjnBWZtg9CXI6LKqsYND7D8wieMV6Sf0CTnn6BoLQgghZR96xYDMBbSFUv_f3pzS8YQNEBv8IIVk59gnDIMCrVf_1LP1mVbe4cZTo9aOm30eAL93l6FRtexpiHq0mB3Ap47vg7mcrlYNoew0K68ImEwTGV6ip7WlQ5XUBFh3wdohslNcI5QUZtV7t67sFD5hk8Bt6-fZ1BfxKAUUy7WE_fU4nl2MeEW7dwSE8nmRs8ggMiv82h326mtzwC7afJ7sAiY04IT2veinDOADPNBRtUtIQm980N85Go2Tk1PUa-qhQ\"}",
}

# File containing deprovisioned users
DEPROVISIONED_USERS_FILE = "Output/okta_users_DEPROVISIONED.json"

# Logs directory
LOGS_DIR = "Logs"
os.makedirs(LOGS_DIR, exist_ok=True)

# Create log file with timestamp
log_file_path = f"{LOGS_DIR}/deletion_log_{int(time.time())}.txt"

def log_message(message):
    """Log a message to both console and log file"""
    print(message)
    with open(log_file_path, "a") as log_file:
        log_file.write(f"{message}\n")

async def delete_user(client, user_id, user_login):
    """Delete a user from Okta"""
    try:
        # Attempt to delete the user
        _, err = await client.deactivate_or_delete_user(user_id)
        
        if err:
            log_message(f"ERROR: Failed to delete user {user_login} (ID: {user_id}): {err}")
            return False
        else:
            log_message(f"SUCCESS: Deleted user {user_login} (ID: {user_id})")
            return True
    except Exception as e:
        log_message(f"EXCEPTION: Error while deleting user {user_login} (ID: {user_id}): {str(e)}")
        return False

async def main():
    log_message("=== STARTING DEPROVISIONED USER DELETION PROCESS ===")
    
    # Initialize Okta client
    log_message("Initializing Okta client...")
    okta_client = OktaClient(config)
    
    # Read the list of deprovisioned users
    try:
        log_message(f"Reading deprovisioned users from {DEPROVISIONED_USERS_FILE}...")
        with open(DEPROVISIONED_USERS_FILE, "r") as f:
            deprovisioned_users = json.load(f)
        
        log_message(f"Found {len(deprovisioned_users)} deprovisioned users")
    except FileNotFoundError:
        log_message(f"ERROR: File {DEPROVISIONED_USERS_FILE} not found!")
        return
    except json.JSONDecodeError:
        log_message(f"ERROR: File {DEPROVISIONED_USERS_FILE} contains invalid JSON!")
        return
    
    # Delete users with progress indicators
    successful_deletions = 0
    failed_deletions = 0
    total_users = len(deprovisioned_users)
    
    log_message(f"Starting deletion of {total_users} users...")
    
    for index, user in enumerate(deprovisioned_users):
        user_id = user.get("id")
        user_login = user.get("login")
        
        # Progress indicator
        progress = (index + 1) / total_users * 100
        log_message(f"Processing user {index + 1}/{total_users} ({progress:.1f}%): {user_login}")
        
        # Validate user data
        if not user_id or not user_login:
            log_message(f"WARNING: Skipping entry with missing user ID or login: {user}")
            failed_deletions += 1
            continue
        
        # Delete the user
        success = await delete_user(okta_client, user_id, user_login)
        
        if success:
            successful_deletions += 1
        else:
            failed_deletions += 1
        
        # Add a small delay between API calls to prevent rate limiting
        # if index < total_users - 1:
        #     await asyncio.sleep(0.1)
    
    # Final summary
    log_message("\n=== DELETION PROCESS COMPLETE ===")
    log_message(f"Total users processed: {total_users}")
    log_message(f"Successful deletions: {successful_deletions}")
    log_message(f"Failed deletions: {failed_deletions}")
    log_message(f"Detailed log saved to: {log_file_path}")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())