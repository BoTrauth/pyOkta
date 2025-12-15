import asyncio
import json
import os
from okta.client import Client as OktaClient

# Reusing the same configuration from GetOktaObjects.py
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

okta_client = OktaClient(config)

# Define all possible user statuses
USER_STATUSES = [
    "STAGED", 
    "PROVISIONED", 
    "ACTIVE", 
    "RECOVERY", 
    "PASSWORD_EXPIRED",
    "LOCKED_OUT", 
    "SUSPENDED", 
    "DEPROVISIONED"
]

async def get_users_by_status(client, status):
    """Retrieves users with the specified status"""

    users, resp, err = await client.list_users(
        query_params={'filter': f'status eq "{status}"'}
    )
        
    if err:
        print(f"Error fetching users with status {status}: {err}")
        return []
    
    all_users = list(users)
    
    # Handle pagination
    while resp.has_next():
        users_page, err = await resp.next()
        if err:
            print(f"Error fetching next page for status {status}: {err}")
            break
        all_users.extend(users_page)
        
    return all_users

async def get_all_users_by_status(client):
    """Retrieves all users and organizes them by status"""
    users_by_status = {}
    
    # Initialize the dictionary with empty lists for each status
    for status in USER_STATUSES:
        users_by_status[status] = []
    
    # Get users for each status
    for status in USER_STATUSES:
        print(f"Fetching users with status: {status}...")
        users = await get_users_by_status(client, status)
        users_by_status[status] = users
        print(f"Found {len(users)} users with status {status}")
        
    return users_by_status

def save_users_to_json_by_status(users_by_status):
    """Save users to separate JSON files based on their status"""
    output_dir = "Output"
    os.makedirs(output_dir, exist_ok=True)
    
    for status, users in users_by_status.items():
        if not users:
            print(f"No users found with status {status}, skipping file creation")
            continue
            
        # Create a list of user dictionaries with key information
        users_data = []
        for user in users:
            users_data.append({
                "id": user.id,
                "login": user.profile.login,
                "status": user.status
            })
        
        # Save to JSON file
        filename = f"{output_dir}/okta_users_{status}.json"
        with open(filename, "w") as f:
            json.dump(users_data, f, indent=4)
        
        print(f"Saved {len(users_data)} users with status {status} to {filename}")

async def main():
    print("Starting Okta user retrieval process...")
    
    # Get all users organized by status
    users_by_status = await get_all_users_by_status(okta_client)
    
    # Save users to separate JSON files by status
    save_users_to_json_by_status(users_by_status)
    
    print("Process completed!")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())