# API Reference

## Package Structure

```
src/pyokta_manager/
├── __init__.py              # Package initialization
├── cli.py                   # CLI interface
├── config.py                # Configuration management
├── client.py                # Okta client wrapper
├── user_operations.py       # User operations
├── group_operations.py      # Group operations
├── app_operations.py        # Application operations
└── cleanup_operations.py    # Bulk cleanup operations
```

## Core Modules

### config.py

#### OktaConfig
Configuration manager for Okta credentials.

```python
from pyokta_manager.config import OktaConfig

config = OktaConfig()  # Auto-loads from .env
config = OktaConfig("/path/to/.env")  # Custom path
```

**Properties:**
- `org_url: str` - Okta organization URL
- `client_id: str` - OAuth 2.0 client ID
- `private_key: str` - Private key JSON
- `scopes: List[str]` - API scopes
- `protected_user_emails: List[str]` - Protected user emails
- `protected_app_ids: List[str]` - Protected app IDs
- `protected_group_ids: List[str]` - Protected group IDs

**Methods:**
- `get_client_config() -> dict` - Get config for Okta client

### client.py

#### OktaClientWrapper
Wrapper around Okta SDK with helper methods.

```python
from pyokta_manager.client import OktaClientWrapper
from pyokta_manager.config import OktaConfig

config = OktaConfig()
client = OktaClientWrapper(config)
```

**Methods:**
- `async get_all_users(query_params: dict = None) -> List` - Get all users with pagination
- `async get_all_groups() -> List` - Get all groups with pagination
- `async get_all_applications() -> List` - Get all applications with pagination
- `is_protected_user(user) -> bool` - Check if user is protected
- `is_protected_app(app_id: str) -> bool` - Check if app is protected
- `is_protected_group(group_id: str) -> bool` - Check if group is protected

### user_operations.py

**Functions:**
- `async list_users(client, status=None, output_file=None)` - List users
- `async export_users_by_status(client, output_dir="Output")` - Export by status
- `async activate_user(client, user_id, send_email=True)` - Activate user
- `async deactivate_user(client, user_id)` - Deactivate user
- `async delete_user(client, user_id)` - Delete user
- `async create_user(client, first_name, last_name, email, password=None, activate=False)` - Create user
- `async delete_deprovisioned_users(client, log_dir="Logs")` - Delete deprovisioned users

### group_operations.py

**Functions:**
- `async list_groups(client, output_file=None)` - List groups
- `async create_group(client, name, description="")` - Create group
- `async delete_group(client, group_id)` - Delete group
- `async add_user_to_group(client, group_id, user_id)` - Add user to group
- `async remove_user_from_group(client, group_id, user_id)` - Remove user from group

### app_operations.py

**Functions:**
- `async list_applications(client, output_file=None)` - List applications
- `async delete_application(client, app_id)` - Delete application

### cleanup_operations.py

**Functions:**
- `async cleanup_all(client, skip_apps=False, skip_groups=False, skip_users=False)` - Cleanup all resources

## CLI Commands

### Main Command
```
okta-manager [--env-file PATH] COMMAND [ARGS]...
```

### User Commands
```
users list [--status STATUS] [--output PATH]
users export [--output-dir DIR]
users create -f FIRST -l LAST -e EMAIL [-p PASSWORD] [--activate]
users activate USER_ID [--send-email/--no-send-email]
users deactivate USER_ID
users delete USER_ID
users delete-deprovisioned [--log-dir DIR]
```

### Group Commands
```
groups list [--output PATH]
groups create -n NAME [-d DESCRIPTION]
groups delete GROUP_ID
groups add-user GROUP_ID USER_ID
groups remove-user GROUP_ID USER_ID
```

### Application Commands
```
apps list [--output PATH]
apps delete APP_ID
```

### Cleanup Command
```
cleanup [--skip-apps] [--skip-groups] [--skip-users]
```
