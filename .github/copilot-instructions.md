# PyOkta Manager - AI Agent Instructions

## Project Architecture

**PyOkta Manager** is a CLI tool for managing Okta resources (users, groups, apps) with multi-environment support and bulk operations. Built with:
- **Okta SDK** (async): All operations are async using `okta.client.Client`
- **Click**: CLI framework with custom `@async_command` decorator (wraps `asyncio.run()`)
- **Multi-environment**: Separate `.env.{dev,qa,prev}` files for different Okta instances

### Core Components

```
src/pyokta_manager/
├── cli.py                    # Click commands with @async_command decorator
├── client.py                 # OktaClientWrapper with pagination & protection checks
├── config.py                 # OktaConfig loads .env.{environment} files
├── user_operations.py        # User CRUD + bulk delete operations
├── group_operations.py       # Group CRUD + bulk delete operations
├── app_operations.py         # Application CRUD + bulk delete operations
└── cleanup_operations.py     # Cleanup all resources (respects protections)
```

**Key Pattern**: CLI commands use `@async_command` decorator → wrap async operations → operations import at function level to avoid circular deps.

## Critical Workflows

### Development Setup
```powershell
# Use UV package manager (preferred)
uv venv && .\.venv\Scripts\Activate.ps1 && uv pip install -e .

# Configure environment
Copy-Item .env.template .env.dev
# Edit .env.dev with credentials
```

### Running Commands
```powershell
# Always specify environment with --env
okta-manager --env dev users list
okta-manager --env qa apps delete-all
okta-manager --env prev cleanup
```

**Important**: The `--env` flag is required and selects which `.env.{environment}` file to load.

### Testing
No test suite currently exists. Manual testing against dev environment.

## Project-Specific Conventions

### Async Everywhere
All operations are async. CLI uses custom decorator pattern:
```python
@async_command  # Wraps asyncio.run()
async def command(client, ...):
    await some_operation(client, ...)
```

### Protected Resources System
Three levels of protection via environment variables:
- `PROTECTED_USER_EMAILS`: Users to skip during deletion (email or login)
- `PROTECTED_APP_IDS`: Apps to skip during deletion
- `PROTECTED_GROUP_IDS`: Groups to skip during deletion

**Implementation**: `OktaClientWrapper` has `is_protected_user()`, `is_protected_app()`, `is_protected_group()` methods checked before deletion.

### Pagination Pattern
SDK responses use `has_next()` and `next()`. Wrapper methods in `client.py` handle this:
```python
async def get_all_users(self, query_params=None):
    all_users = []
    users, resp, err = await self.client.list_users(query_params)
    all_users.extend(users)
    while resp.has_next():
        users, err = await resp.next()
        all_users.extend(users)
    return all_users
```

### Logging Pattern
Bulk operations create timestamped logs in `Logs/` directory:
```python
log_file = Path(log_dir) / f"delete_all_log_{int(time.time())}.txt"
```

### Error Handling
Operations return `(result, response, error)` tuples from SDK. Check `err` before proceeding:
```python
user, resp, err = await client.client.get_user(user_id)
if err:
    print(f"❌ Failed: {err}")
    return None
```

**Special case**: `E0000007` error code means "already deactivated" - handle gracefully in app/user operations.

## Configuration Management

### Environment Files
- `.env.template`: Template with all variables
- `.env.dev`, `.env.qa`, `.env.prev`: Environment-specific configs
- `OktaConfig.__init__()` validates required vars: `OKTA_ORG_URL`, `OKTA_CLIENT_ID`, `OKTA_PRIVATE_KEY`

### Private Key Format
`OKTA_PRIVATE_KEY` must be JSON string with fields: `d`, `p`, `q`, `dp`, `dq`, `qi`, `kty`, `e`, `kid`, `n`.

## Key Integration Points

### Okta SDK Usage
- **Client creation**: `OktaClient(config.get_client_config())` with `authorizationMode: "PrivateKey"`
- **User status values**: `STAGED`, `PROVISIONED`, `ACTIVE`, `RECOVERY`, `PASSWORD_EXPIRED`, `LOCKED_OUT`, `SUSPENDED`, `DEPROVISIONED`
- **Deactivation required**: Apps and active users must be deactivated before deletion

### Click Context Pattern
```python
@click.pass_obj  # Passes OktaClientWrapper from ctx.obj
async def command(client, ...):
    # client is OktaClientWrapper instance
```

### Lazy Imports
Operations modules imported at function level in CLI to avoid circular dependencies:
```python
async def users_list(client, ...):
    from .user_operations import list_users  # Import here
    await list_users(client, ...)
```

## Output Conventions

### JSON Export Structure
User/group/app data converted to dicts with specific fields (see `*_operations.py` files). Example:
```python
{
    "id": u.id,
    "status": u.status,
    "profile": {"login": u.profile.login, "email": u.profile.email, ...}
}
```

### Output Directories
- `Output/`: User exports by status (`okta_users_ACTIVE.json`, etc.)
- `Logs/`: Deletion operation logs with timestamps
- `CustomLogs/`: (appears unused)

### Console Output
- ✅ for success, ❌ for errors
- Summary line after bulk operations: `📊 Summary: X deleted, Y failed, Z protected/skipped`
- Status printed during operations with indentation for clarity

## When Adding Features

1. **New CLI commands**: Add to appropriate group (`users`, `groups`, `apps`, `cleanup`), use `@async_command` and `@click.pass_obj`
2. **New operations**: Create async functions in corresponding `*_operations.py` file, import lazily in CLI
3. **New config**: Add to `OktaConfig` as `@property`, load from env var
4. **Bulk operations**: Follow logging pattern with timestamped files, track protected resources, provide summary
5. **SDK calls**: Always handle `(result, resp, err)` tuple pattern, implement pagination for list operations
