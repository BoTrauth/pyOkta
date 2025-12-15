# Archived Old Scripts

These scripts have been refactored into the new `pyokta_manager` package structure.

## Migration Guide

| Old Script | New Functionality |
|------------|------------------|
| `app.py` | `okta-manager groups list --output Output/groups.json` |
| `app2.py` | `okta-manager cleanup` |
| `analyze_okta_users.py` | Use `okta-manager users list` and analyze JSON output |
| `avtivate_user.py` | `okta-manager users activate USER_ID` / `okta-manager users deactivate USER_ID` |
| `CreateOktaObjects.py` | `okta-manager users create` / `okta-manager groups create` |
| `delete_deprovisioned_users.py` | `okta-manager users delete-deprovisioned` |
| `GetOktaObjects.py` | `okta-manager users list` / `okta-manager groups list` / `okta-manager apps list` |
| `okta_users_by_status.py` | `okta-manager users export` |

## Why Archive?

These scripts have been replaced by a more maintainable, professional package with:
- Centralized configuration management
- No hardcoded credentials
- Consistent CLI interface
- Better error handling
- Type hints and documentation
- Support for modern tools like `uv`
