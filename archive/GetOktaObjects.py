import asyncio
from okta.client import Client as OktaClient
import json

# Okta Developer
config = {
    'orgUrl': 'https://integrator-1715139.okta.com',
    'authorizationMode': 'PrivateKey',
    'clientId': '0oaw7uwv0z8OaDC8C697',
    'scopes': [
        'okta.users.manage', 
        'okta.groups.manage', 
        'okta.apps.manage'
    ],
    'privateKey': "{\"d\": \"EGpjpRu8N9o76VljYQXwJtn08EGFzgWesxY_bvE15ReTVQ-VbS2kBdEgUKqvF-DLTj0UHpdj0YDvuT22Za7YSGwMhXmvO2Dsj0uUNlgg5Oe3QNRvxR-6dICG8FGbOdlGC9MnTur3rPHgdK-QWtoN5lABEge--JxBWywSZZAHc241sXRAJwK__FUeQvLYLf3vqE8l91f0gFIVzp4HDpm5sHi0QawqmWUQsh4KmUPmF5OI6bnv6zLIUqnfKjGjzr5xoNiydm7w6vfJlAvUM9c5LmXduNOfQpj1Ho0LAXwmZH77aWTbqtEf3iEw7D3prAf0zRSfGyawtfxhbm5E3uKz0Q\", \"p\": \"-HkoGwogpJ2CkvpTsZSHyzEJ17k_7ZGiOZG6tCtZo16AGHs6HbaPEPBXkR3YYxtbZVeTPBNfEQB974z4jGq2YeY1CjJZap7XIzdx7B31quw0qL1p4VmolrX79gM5T8Y-U-3UIMI_nYwKmJfkHm0BbtXvVeVLd5SwFBeIEkVms5k\", \"q\": \"1v86Zs2qAej2TXXM5RWOF2VjQ5u3IHsfjAU4BbgHrkL8TL8BYC2_SWWwCrJ_toVK7BWk1ITJWkk0b54BYRx_o6UeLUwZj2agWxzHG1OD-j7K51vR_1tLbOwxEtfzfkwzmpKT0pqgGghmR8jgc7DgFodCUDGhiSE1dLmCNS2xueU\", \"dp\": \"CCbBYBG2_G-GZxf7QuoiglH7hq43IK4UalsTivGZITjqbuMsBumETAP2e3ZFMQsmtm5nECN6jO49M2ymgsTFcvTAbLM2J79KQ4eAH0TkWFUjbR25qYDtfPQ_bdSxPqK8TLiSqvh0adC8UEE7ZJwi3eX60hCRpzyjgiU7e433TpE\", \"dq\": \"cyP5CPl35NH4pn9CHiWvFUSNJrYMGu8VdA2PdTCbnG3vZMKeX_3gBdTZtMDnuL4l482rms0KcLnnxScfofx7Nw7E3Il23t-dXW5KC45sjeZ3D_SSwGkKOek8VtUkaC0zLcL2O8HnoEmDTUp9OjgtqqMBlqUd16zbTgnTe9te5Sk\", \"qi\": \"Vzxp0mGnqkppYf3hJNZlKI4ExEcM3X54d5nKtyqo0_yPHgArwJy7LgfuWwvr5UeUpO203KkeTM4VO_dwcKgv_tEKH3qJXc_U6hDoM9jS2DHQWUCw7-u59-UbtUwNRbWyBVM4yUh53pNdOMmTfE60pkPvRIxy3sDIfR8vP8EJNbg\", \"kty\": \"RSA\", \"e\": \"AQAB\", \"kid\": \"9KR8ggZYbUY-z0evbMeWYsQg4ZO3iWtc332UaiMm5bk\", \"n\": \"0K0A5Mhggp3xbiBcrY_8Q-80uFhKdgDH2YOjZsthtm8AZ229DWKzYQ853QrWfaxKIzmX9HScqJGmxwquzsdEQ9iexnvtFZVJbUY2qshsGiYxbzz7b0dChnd-V18XyGkQ9loVAgZV8x3v_Thi1eMv9fb7Tyq6kv38vnNtmMl0MT-pqmKi-ezQPXvC68Z4RFjBAfiHYd8jUPBBg_ixhw8z5ZVb1h9mbrrBeuLTEi_-_GtzYRh3Vri-lSiE3B0CeiOkiAoDyLRXS4qJ6lPOTEeE0sMv_-B9oTnQ6R394jWDcl-nXRbkByIKnec7xBiPInSkeaSPtVebUoPoPtbAXnE43Q\"}"
}

okta_client = OktaClient(config)

async def get_all_users(client):
    """Retrieve all users using built-in pagination."""
    all_users = []
    query_params = {
    'filter': (
        'status eq "STAGED" or '
        'status eq "PROVISIONED" or '
        'status eq "ACTIVE" or '
        'status eq "RECOVERY" or '
        'status eq "PASSWORD_EXPIRED" or '
        'status eq "LOCKED_OUT" or '
        'status eq "SUSPENDED" or '
        'status eq "DEPROVISIONED"')
    }
    
    # Get the first page of users.
    users, resp, err = await client.list_users(query_params=query_params)
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
    # Get the first page of groups.
    groups, resp, err = await client.list_groups()
    if err:
        print("Error fetching groups:", err)
        return all_groups

    # Add the first page to our list.
    all_groups.extend(groups)
    # Continue retrieving pages while available.
    while resp.has_next():
        groups, err = await resp.next()
        if err:
            print("Error fetching next page:", err)
            break
        all_groups.extend(groups)
    return all_groups

async def get_all_applications(client):
    """Retrieve all applications using built-in pagination."""
    all_applications = []
    # Get the first page of applications.
    applications, resp, err = await client.list_applications()
    if err:
        print("Error fetching applications:", err)
        return all_applications

    # Add the first page to our list.
    all_applications.extend(applications)
    # Continue retrieving pages while available.
    while resp.has_next():
        applications, err = await resp.next()
        if err:
            print("Error fetching next page:", err)
            break
        all_applications.extend(applications)
    return all_applications

def save_user_to_json(users):
    """Save data to a JSON file."""
    print(f"\n=== Retrieved {len(users)} Users ===")
    
    # Create a list of user dictionaries with key information
    users_data = []
    for user in users:
        users_data.append({
            "id": user.id,
            "login": user.profile.login,
            # "email": user.profile.email,
            "status": user.status
        })
    
    # Save to JSON file
    with open("okta_users.json", "w") as f:
        json.dump(users_data, f, indent=4)
    
    print(f"Users data saved to okta_users.json")

if __name__ == "__main__":
    
    # Example usage of the creation functions
    loop = asyncio.get_event_loop()

    # Get all users
    users = loop.run_until_complete(get_all_users(okta_client))
    print(f"\n=== Retrieved {len(users)} Users ===")
    for user in users:
        print(f"User ID: {user.id}, User Name: {user.profile.login}, User Status: {user.status}")
    
    # Get and print all groups
    groups = loop.run_until_complete(get_all_groups(okta_client))
    print(f"\n=== Retrieved {len(groups)} Groups ===")
    for group in groups:
        print(f"Group ID: {group.id}, Group Name: {group.profile.name}")
    
    # Get and print all applications
    applications = loop.run_until_complete(get_all_applications(okta_client))
    print(f"\n=== Retrieved {len(applications)} Applications ===")
    for app in applications:
        print(f"Application ID: {app.id}, Application Name: {app.name}, Status: {app.status}, Description: {app.label}")
        # print(f"Application ID: {app.id}, Name: {app.name}, Description: {app.label}  Status: {app.status}")