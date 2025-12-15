import json

# Load the JSON file
file_path = "okta_users.json"
try:
    with open(file_path, 'r') as file:
        users_data = json.load(file)
except json.JSONDecodeError as e:
    print(f"Error parsing JSON file: {e}")
    users_data = []
except FileNotFoundError:
    print(f"File not found: {file_path}")
    users_data = []

# Count the number of objects
total_objects = len(users_data)
print(f"Total number of objects in okta_users.json: {total_objects}")

# Check for 'dave' or 'eyal' in login fields
dave_count = 0
eyal_count = 0
matches = []

for user in users_data:
    if 'login' in user:
        login = user['login'].lower()
        if 'dave.brann' in login:
            dave_count += 1
            matches.append(user['login'])
        if 'eyal' in login:
            eyal_count += 1
            matches.append(user['login'])

print(f"Number of logins containing 'dave': {dave_count}")
print(f"Number of logins containing 'eyal': {eyal_count}")

if matches:
    print("\nMatching logins:")
    for login in matches:
        print(f"  - {login}")
else:
    print("\nNo logins containing 'dave' or 'eyal' were found.")