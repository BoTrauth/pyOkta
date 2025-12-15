from okta.client import Client as OktaClient
import asyncio, json, time, os

config = {
    'orgUrl': 'https://dev-520699.oktapreview.com',
    'authorizationMode': 'PrivateKey',
    'clientId': '0oa25xglftsc8nNHv0h8',
    'scopes': ['okta.users.manage'],
    'privateKey': "{\"d\": \"FfWD0vuFUTHkJxVmgO4u0ZrGqTO_76_YNB_nC3BLCLOXzzjO65ytU5H_BgcTzL-2lvekNTqHMzBpnr5cSidugqoCV4i5ah62hmazOi6mRl6mmhLpptj9cTenwzbQhUhFK20cdOfdnuJspUo7d7_hzGodobUrVBzJIcs3ml3wFtMBeld6BSD8jIQhHp0nrHAOP2I6lkgC4OL5JzVYWFFY7A_f_HBPm-QXLjHLpQ0_hq2rDy7hADwknV5VBYz5GebU0ps1IFDgVfSwRqyaMG-SUGUafXYxrKhoTb1AylN0yQ6gGj4mQDRNveSY_j5YmEGXqmY9zgfctDAfQBYp1im7IQ\", \"p\": \"4N2uOWm3-d8CNg4p-OA_zY_pw2_6SrS0qMZj4X2o4ukGDLU2wPtNeMBzVyiOfkGsiSuBl_dfTKJZobEV4upIq3ytHWnkAu-7VcyIm7_01s402tpoXNMt51JAsnnJ6PYIKr6uUcLySCSontWelwG594mCW4ACwkYPBpgk6C62amE\", \"q\": \"x1jsRXLA6swWnFp9hwHBXYVUAoeCwNjjG1dFpsP6jUQX1aRaZpTCD3oYU0FsItMnxzWc40s-mYfV-YhElXkBZNyWza4UtwUwoyFf7gHjWh8dwrfX2Zhe1vvJYuJWJ7tWBz_XyMeaJIUQ3CDavXw5oshRV_3Rj6vbSx2Uo0YXWqU\", \"dp\": \"TH1751G74EZoxSR6SItXiMA8f1uW41Sm44ZgsXKCQXWMtkPqNSkGyF2Gno5QMkh6vUpMUfo2s6XCIYtQa5jQUW0eohPEGO-dZOknSvu3-F26gvuqZnD7e2VyVoOxGAqg6pFkULGkor-9kBIQWUOgE8D109QunBEiyVZ1r3k8WeE\", \"dq\": \"PhKzZ6Cm77XjKIaI5dwnEO7uTOdTUKd4eFABkT8fKpPUdCL8P0r87oLPRkVt3Z4wmbhZBPGuKXKBr3S-HmkShQynLJ6TNrY4AePnkh4mZC6iPrquTMREa971Q4RE3ZRY4mL_1zZICi0hJdpZIn2nGMgVhDe15G3YGBi66uhtZz0\", \"qi\": \"hnVclED8kBMm83RFVi8hYEF2JhNo2ATBImlDovxjkWHrDkNuk8lkADIJKONwLHQSZ0z0UHZAkzHlVOZ2oMqaHZa9t_nsEd5MC1_5YuvYlhcFYof29Rodmtcn4zRUn2bQ0Tj-NvUazS6iGvwcKQi7SHMq4yYZvEiaeHUmWBR5J50\", \"kty\": \"RSA\", \"e\": \"AQAB\", \"kid\": \"o9jT-aVK-SswdaqpwwY-jFgavJGEsnIJfCMd6qPEf_A\", \"n\": \"rxpuK-ITaX96N6HrV-oAYfrabTv4-V3KuErK1SyAlHjnBWZtg9CXI6LKqsYND7D8wieMV6Sf0CTnn6BoLQgghZR96xYDMBbSFUv_f3pzS8YQNEBv8IIVk59gnDIMCrVf_1LP1mVbe4cZTo9aOm30eAL93l6FRtexpiHq0mB3Ap47vg7mcrlYNoew0K68ImEwTGV6ip7WlQ5XUBFh3wdohslNcI5QUZtV7t67sFD5hk8Bt6-fZ1BfxKAUUy7WE_fU4nl2MeEW7dwSE8nmRs8ggMiv82h326mtzwC7afJ7sAiY04IT2veinDOADPNBRtUtIQm980N85Go2Tk1PUa-qhQ\"}",
}

okta_client = OktaClient(config)

async def main():
    groups, resp, err = await okta_client.list_groups()
    path = os.path.join('Output', time.strftime(f"%Y-%m-%d_%H-%M-%S") + ".json")
    with open(path, 'w') as writer:
        json.dump(resp, writer, indent=2, default=str)

if __name__ == "__main__":
    asyncio.run(main())