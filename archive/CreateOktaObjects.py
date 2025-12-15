import asyncio
import logging
from okta.client import Client as OktaClient

# Update the configuration with required scopes

# config = {
#     'orgUrl': 'https://dev-520699.oktapreview.com',
#     'authorizationMode': 'PrivateKey',
#     'clientId': '0oa25xglftsc8nNHv0h8',
#     'scopes': [
#         'okta.users.manage', 
#         'okta.groups.manage', 
#         'okta.apps.manage'
#     ],
#     'privateKey': "{\"d\": \"FfWD0vuFUTHkJxVmgO4u0ZrGqTO_76_YNB_nC3BLCLOXzzjO65ytU5H_BgcTzL-2lvekNTqHMzBpnr5cSidugqoCV4i5ah62hmazOi6mRl6mmhLpptj9cTenwzbQhUhFK20cdOfdnuJspUo7d7_hzGodobUrVBzJIcs3ml3wFtMBeld6BSD8jIQhHp0nrHAOP2I6lkgC4OL5JzVYWFFY7A_f_HBPm-QXLjHLpQ0_hq2rDy7hADwknV5VBYz5GebU0ps1IFDgVfSwRqyaMG-SUGUafXYxrKhoTb1AylN0yQ6gGj4mQDRNveSY_j5YmEGXqmY9zgfctDAfQBYp1im7IQ\", \"p\": \"4N2uOWm3-d8CNg4p-OA_zY_pw2_6SrS0qMZj4X2o4ukGDLU2wPtNeMBzVyiOfkGsiSuBl_dfTKJZobEV4upIq3ytHWnkAu-7VcyIm7_01s402tpoXNMt51JAsnnJ6PYIKr6uUcLySCSontWelwG594mCW4ACwkYPBpgk6C62amE\", \"q\": \"x1jsRXLA6swWnFp9hwHBXYVUAoeCwNjjG1dFpsP6jUQX1aRaZpTCD3oYU0FsItMnxzWc40s-mYfV-YhElXkBZNyWza4UtwUwoyFf7gHjWh8dwrfX2Zhe1vvJYuJWJ7tWBz_XyMeaJIUQ3CDavXw5oshRV_3Rj6vbSx2Uo0YXWqU\", \"dp\": \"TH1751G74EZoxSR6SItXiMA8f1uW41Sm44ZgsXKCQXWMtkPqNSkGyF2Gno5QMkh6vUpMUfo2s6XCIYtQa5jQUW0eohPEGO-dZOknSvu3-F26gvuqZnD7e2VyVoOxGAqg6pFkULGkor-9kBIQWUOgE8D109QunBEiyVZ1r3k8WeE\", \"dq\": \"PhKzZ6Cm77XjKIaI5dwnEO7uTOdTUKd4eFABkT8fKpPUdCL8P0r87oLPRkVt3Z4wmbhZBPGuKXKBr3S-HmkShQynLJ6TNrY4AePnkh4mZC6iPrquTMREa971Q4RE3ZRY4mL_1zZICi0hJdpZIn2nGMgVhDe15G3YGBi66uhtZz0\", \"qi\": \"hnVclED8kBMm83RFVi8hYEF2JhNo2ATBImlDovxjkWHrDkNuk8lkADIJKONwLHQSZ0z0UHZAkzHlVOZ2oMqaHZa9t_nsEd5MC1_5YuvYlhcFYof29Rodmtcn4zRUn2bQ0Tj-NvUazS6iGvwcKQi7SHMq4yYZvEiaeHUmWBR5J50\", \"kty\": \"RSA\", \"e\": \"AQAB\", \"kid\": \"o9jT-aVK-SswdaqpwwY-jFgavJGEsnIJfCMd6qPEf_A\", \"n\": \"rxpuK-ITaX96N6HrV-oAYfrabTv4-V3KuErK1SyAlHjnBWZtg9CXI6LKqsYND7D8wieMV6Sf0CTnn6BoLQgghZR96xYDMBbSFUv_f3pzS8YQNEBv8IIVk59gnDIMCrVf_1LP1mVbe4cZTo9aOm30eAL93l6FRtexpiHq0mB3Ap47vg7mcrlYNoew0K68ImEwTGV6ip7WlQ5XUBFh3wdohslNcI5QUZtV7t67sFD5hk8Bt6-fZ1BfxKAUUy7WE_fU4nl2MeEW7dwSE8nmRs8ggMiv82h326mtzwC7afJ7sAiY04IT2veinDOADPNBRtUtIQm980N85Go2Tk1PUa-qhQ\"}",
# }

config = {
    'orgUrl': 'https://dev-79927172.okta.com',
    'authorizationMode': 'PrivateKey',
    'clientId': '0oaohqp4v4sS3USoc5d7',
    'scopes': [
        'okta.users.manage', 
        'okta.groups.manage', 
        'okta.apps.manage'
    ],
    'privateKey': "{\r\n    \"d\": \"C_i9xhaI8lGqaFX4htfxb0WFhIbz5ifU1iy3X00IyuYt29F_RndJdEZ1rvskMPYMpOJtePqAZtwoushKGGPzdWFCPyxMp65MaMVHsal0aKVQ8dVQVRvcnJgt4_bAWjVDTwJTMxrwsRU4HE034BF27f2kAlxIfGHEWKIC7ytjOJfbrQgSauCIfR60SxnqlAQbZz3RHEyTNjd-WMBRNOblzMpfL3TSrD97MM4zskqzBoZyWDytv7yuVhE1rI3ibq6z60ws90FmAVE0-FjxW74YTjF4NYIIb3ZOS1H9VbrrUzO1xNfpcFnP16DTMEzRK9sia2LmlTEjOuaCXJYlx16W2Q\",\r\n    \"p\" : \"yVgcfPVwTrFJ7df_jfq_-6ROTvUwzygKrHBmBKveXMcyhy88ySFwkN3YBe9c5yLL4JJFQL0IBAZihqJeixjnp8ojB-zM_wzth8dok0ANonVMiQN8f7a4E95of80wo7laFhkATldHXKoHc8zdg83LTn57Lq4EjHlNuu6WZ-Ssjy8\",\r\n    \"q\" : \"xEs3zs3n-_NYME0sd4VG3tsrB61nnAjGWFkzSJQTR7OU3mqrEe5T7qi0IsJWF9J80rNxN0LQh9VfCaBQTantuwhk6oecTwNG1AVe46u0uCdexsTo5PKOqcnWxUfWzlgryGTmyFPOy7GYnnwbnithebl0mtmzZGf0fGXg99hD6mM\",\r\n    \"dp\" : \"jbTK0BO6CFh0zMXh4d5iMkyQpLeis5nd8UFmO9FuveOgp05SvMghPoQ0XvD5dN-jmBm6Tfb85kBMJa-vVLyhhhEZGKHMIZHKt25cJo7FSdq-lAv1GrnR0oINEC2tFv4D7luIQJri6c_tUM4V9YbomQUh01e8cdWKJI95IgPqgxc\",\r\n    \"dq\" : \"G0htIFRkOxOunUAMvywKFq2VxIJolTpu_xae1yalq2Cdf3CKCHr8tX5DU1V5i-QYr1x7jve9bjPM-tSKdND6lvVquWJR6nWFIbEBaFmUS8hFFxGFYVUJWTYRoOgERjfhFgBYR13Gr28mzFhpqklTSgzp1SAPHBSK2cN7SleH0Qs\",\r\n    \"qi\" : \"mkDe2kpRDaNlLVG_vnnVCPb4Dl93ZLcrkhlIkl61BhjM1E1GEEeX-Qc61s_b1MrQ0FJddMoNTIY54jR3DTZVSvDwzCMZ3QRvi7FHkKLlNnrvKBUSW8mRnIwnD4ZCs8J9ertG485oQjrdIp8JyB9VSogJXD7tg0xn2SBHEIKUR6w\",\r\n    \"kty\" : \"RSA\",\r\n    \"e\" : \"AQAB\",\r\n    \"kid\" : \"UXEtkNUK7og5pb4mDpeV-TwYHOyI4an5pWQyjmiF6gI\",\r\n    \"n\" : \"mmKehJl9rOn5DGk5XdHfHd6XbSIsya7ys5xWcULM6uRVIbfRp3iXTRFTl6q5yLOdAxOQI91pjS0DeQyjPt5xgk2OlG3Obl3mxCPjvMIk-r9MoE17vVCViFn9_gRy5peZ2wHS7-MtCRAUOeVpWJ_v2llc_X78GrX8sgoNj0eM8fSrzm_FtzPJ-IP28c0Z2QWDuKjO7wwNbzcA-K5057Gz-qLsy8a3WZ-YoE7t-6sAobzONNa1Es7g05KaHzKS3uYKKhXp9piEtGI2mf93KC4oDReiv1dJIbUMHvE5Lgb-t-jaMAI0M1xJrV2EsL5ewhTRaav7gXVEZtZHM9mFSulVLQ\"\r\n}",
}

okta_client = OktaClient(config)

# ---------- Creation Functions ----------
async def create_user(client, first_name, last_name, email, password=None):
    """Create a new user in Okta."""
    print(f"\n=== Creating User: {email} ===")
    
    # Build the user profile
    user_profile = {
        "firstName": first_name,
        "lastName": last_name,
        "email": email,
        "login": email
    }
    
    # Build the credentials if password is provided
    credentials = None
    if password:
        credentials = {
            "password": {"value": password}
        }
    
    # Create the user (activate immediately if password provided)
    try:
        create_params = {
            "activate": True if password else False
        }
        
        # Build complete user object
        user_obj = {
            "profile": user_profile
        }
        
        # Add credentials if provided
        if credentials:
            user_obj["credentials"] = credentials
        
        # The correct way to call the create_user method
        user, resp, err = await client.create_user(user_obj, create_params)
        
        if err:
            print(f"Error creating user: {err}")
            return None
        
        print(f"User created successfully: {user.id}")
        return user
            
    except Exception as e:
        print(f"Exception creating user: {e}")
        return None

async def create_group(client, group_name, group_description=None):
    """Create a new group in Okta.
    
    Args:
        client: The Okta client instance
        group_name: Name of the group
        group_description: Optional description of the group
        
    Returns:
        The created group object or None if creation failed
    """
    print(f"\n=== Creating Group: {group_name} ===")
    
    # Build the group profile
    group_profile = {
        "name": group_name,
        "description": group_description or f"Group for {group_name}"
    }
    
    # Create the group
    try:
        group, resp, err = await okta_client.create_group({"profile": group_profile})
        
        if err:
            print(f"Error creating group: {err}")
            return None
        
        print(f"Group created successfully: {group.id}")
        return group
            
    except Exception as e:
        print(f"Exception creating group: {e}")
        return None

async def create_application(client, app_name, app_type="web", app_settings=None):
    """Create a new application in Okta.
    
    Args:
        client: The Okta client instance
        app_name: Name of the application
        app_type: Type of application (web, native, browser, service, etc.)
        app_settings: Optional dictionary with application settings
        
    Returns:
        The created application object or None if creation failed
    """
    print(f"\n=== Creating Application: {app_name} ===")
    
    # Default minimal settings for a web application if none provided
    if not app_settings and app_type == "web":
        app_settings = {
            "app": {
                "requestIntegration": True,
                "url": f"https://example.com/{app_name.lower().replace(' ', '-')}",
                "authRedirectUrls": [f"https://example.com/{app_name.lower().replace(' ', '-')}/callback"]
            }
        }
    
    # Build the application object
    application = {
        "name": f"oidc_{app_type}",  # Standard naming convention for OIDC apps
        "label": app_name,
        "signOnMode": "OPENID_CONNECT",
        "settings": app_settings or {}
    }
    
    # Create the application
    try:
        app, resp, err = await okta_client.create_application(application)
        
        if err:
            print(f"Error creating application: {err}")
            return None
        
        print(f"Application created successfully: {app.id}")
        return app
            
    except Exception as e:
        print(f"Exception creating application: {e}")
        return None

if __name__ == "__main__":
    
    # Example usage of the creation functions
    loop = asyncio.get_event_loop()

    # Create a user
    first_name = "Test4"
    last_name = "User4"
    user = loop.run_until_complete(create_user(okta_client, f"{first_name}", f"{last_name}", f"{first_name}{last_name}@intergraph.com", password="SecurePassword123"))
    
    # # Create a group
    group = loop.run_until_complete(create_group(okta_client, "Test Group 4", "This is a test group."))
    
    # # Create an application
    app = loop.run_until_complete(create_application(okta_client, "Test Application 4", app_type="web"))