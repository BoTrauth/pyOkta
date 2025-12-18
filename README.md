# PyOkta Manager

A professional CLI tool for managing Okta users, groups, and applications with support for bulk operations and cleanup.

## Quick Start

```powershell
# Install with UV
uv venv && .\.venv\Scripts\Activate.ps1 && uv pip install -e .

# Configure credentials for your environment
Copy-Item .env.template .env.dev
# Edit .env.dev with your DEV-Test Okta credentials

# Start using (specify environment)
okta-manager --env dev users list
```

## Multiple Environment Support

PyOkta Manager supports multiple Okta environments:

```powershell
# Use DEV environment
okta-manager --env dev users list

# Use QA environment  
okta-manager --env qa apps list

# Use PREV environment
okta-manager --env prev groups list
```

Configuration files:
- `.env.dev` - DEV-Test environment
- `.env.qa` - QA-Test environment
- `.env.prev` - PREV-Test environment

See [Configuration Guide](docs/configuration.md) for details.

## Common Commands

### Users
```powershell
okta-manager --env dev users list                    # List all users
okta-manager --env dev users list --status ACTIVE    # Filter by status
okta-manager --env dev users export                  # Export by status to files
okta-manager --env dev users create -f John -l Doe -e john@example.com
okta-manager --env dev users activate USER_ID
okta-manager --env dev users deactivate USER_ID
okta-manager --env dev users delete-deprovisioned    # Bulk delete
```

### Groups
```powershell
okta-manager --env dev groups list
okta-manager --env dev groups create -n "Team Name"
okta-manager --env dev groups add-user GROUP_ID USER_ID
okta-manager --env dev groups delete GROUP_ID
```

### Applications
```powershell
okta-manager --env dev apps list
okta-manager --env dev apps delete APP_ID
```

### Cleanup
```powershell
# Delete all non-protected resources
okta-manager --env dev cleanup
```

### Applications
```powershell
okta-manager apps list
okta-manager apps delete APP_ID
```

### Cleanup
```powershell
okta-manager cleanup                       # Full cleanup with safety
okta-manager cleanup --skip-users          # Skip specific resources
```

See [Usage Guide](docs/usage.md) for complete command reference.
```powershell
# List all applications
okta-manager apps list

# Save to file
okta-manager apps list --output apps.json

# Delete an application
okta-manager apps delete APP_ID
```

### Cleanup Operations

```powershell
# Clean up ALL resources (apps, groups, users)
# Protected resources will be skipped
okta-manager cleanup

# Skip specific resource types
okta-manager cleanup --skip-apps
okta-manager cleanup --skip-groups
okta-manager cleanup --skip-users
```

## Project Structure

```
pyOkta/
├── src/
│   └── pyokta_manager/
│       ├── __init__.py
│       ├── cli.py                 # CLI interface
│       ├── config.py              # Configuration management
│       ├── client.py              # Okta client wrapper
│       ├── user_operations.py     # User operations
│       ├── group_operations.py    # Group operations
│       ├── app_operations.py      # Application operations
│       └── cleanup_operations.py  # Bulk cleanup operations
├── tests/                         # Test files
├── Output/                        # JSON export files
├── Logs/                          # Deletion logs
├── pyproject.toml                 # Project configuration
├── .env.example                   # Environment template
├── .gitignore                     # Git ignore rules
└── README.md                      # This file
```

## Development

### Install development dependencies

```powershell
uv pip install -e ".[dev]"
```

### Run tests

```powershell
pytest
```

### Code formatting

```powershell
black src/
ruff check src/
```

## Safety Features

- **Protected Resources**: Configure emails, app IDs, and group IDs that should never be deleted
- **Confirmation Prompts**: Destructive operations require explicit confirmation
- **Comprehensive Logging**: All deletion operations are logged with timestamps
- **Error Handling**: Graceful error handling with clear error messages

## Migration from Old Scripts

The old standalone scripts (`app.py`, `app2.py`, `GetOktaObjects.py`, etc.) have been refactored into a professional package structure. Key improvements:

- ✅ Centralized configuration (no more hardcoded credentials)
- ✅ Modern CLI with `click`
- ✅ Proper package structure
- ✅ Type hints and documentation
- ✅ Consistent error handling
- ✅ Works with `uv` package manager

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
## Project Structure

```
pyOkta/
├── src/pyokta_manager/       # Main package
├── docs/                     # Documentation
├── tests/                    # Tests
├── Output/                   # JSON exports
├── Logs/                     # Deletion logs
├── pyproject.toml            # Package config
└── .env                      # Your credentials
```

## Development

```powershell
# Install dev dependencies
uv pip install -e ".[dev]"

# Format code
black src/

# Lint
ruff check src/
```

See [API Reference](docs/api-reference.md) for package documentation.

## Safety Features

✅ Protected resources (won't be deleted)  
✅ Confirmation prompts for destructive operations  
✅ Comprehensive logging  
✅ Clear error messages

## License

MIT