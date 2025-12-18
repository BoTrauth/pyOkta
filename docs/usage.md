# Usage Guide

## Environment Selection

All commands support the `--env` flag to specify which Okta environment to use:

```powershell
# Use DEV environment
okta-manager --env dev users list

# Use QA environment
okta-manager --env qa apps delete-all

# Use PREV environment
okta-manager --env prev groups list
```

Available environments: `dev`, `qa`, `prev`

## Quick Overview

### List Everything
```powershell
# List all users, groups, and applications
okta-manager --env dev list-all

# Save all to JSON files in a directory
okta-manager --env dev list-all --output-dir Output
```

This command provides a comprehensive view of all resources in the selected environment.

## User Management

### List Users
```powershell
# List all users (displays formatted list with email, name, and status)
okta-manager --env dev users list

# Filter by status
okta-manager --env dev users list --status ACTIVE
okta-manager --env dev users list --status DEPROVISIONED

# Save to JSON
okta-manager --env dev users list --output users.json
```

**Output format:**
```
Found 18 users

  email@example.com                         John Doe                       ACTIVE
  jane@example.com                          Jane Smith                     PROVISIONED
  ...
```

### Export Users
```powershell
# Export users grouped by status to separate files
okta-manager --env dev users export --output-dir Output
```

### Create User
```powershell
# Create user
okta-manager --env dev users create -f John -l Doe -e john@example.com

# Create and activate immediately
okta-manager --env dev users create -f Jane -l Smith -e jane@example.com --activate

# Create with password
okta-manager --env dev users create -f Bob -l Johnson -e bob@example.com -p SecurePass123
```

### Manage User Status
```powershell
# Activate user
okta-manager --env dev users activate USER_ID

# Activate without email
okta-manager --env dev users activate USER_ID --no-send-email

# Deactivate user
okta-manager --env dev users deactivate USER_ID
```

### Delete Users
```powershell
# Delete single user (requires confirmation)
okta-manager --env dev users delete USER_ID

# Delete all deprovisioned users (requires confirmation)
okta-manager --env dev users delete-deprovisioned --log-dir Logs

# Delete ALL users except protected ones (requires confirmation)
okta-manager --env dev users delete-all --log-dir Logs
```

**Note:** `delete-all` will:
- Automatically deactivate users if needed before deletion
- Skip users listed in `PROTECTED_USER_EMAILS` in your `.env` file
- Create a detailed log file with timestamps
- Show progress for each user (PROTECTED/SUCCESS/ERROR)

## Group Management

### List Groups
```powershell
# List all groups (displays formatted list with name, ID, and description)
okta-manager --env dev groups list

# Save to JSON
okta-manager --env dev groups list --output groups.json
```

**Output format:**
```
Found 5 groups

  Engineering Team                          00ga8odrxaV0HtAb90h7      Engineering department
  Marketing                                 00g1m0nlnaby0URcX0h8      Marketing team
  ...
```

### Create Group
```powershell
okta-manager --env dev groups create -n "Engineering Team" -d "Engineering department"
```

### Delete Groups
```powershell
# Delete single group (requires confirmation)
okta-manager --env dev groups delete GROUP_ID

# Delete ALL groups except protected ones (requires confirmation)
okta-manager --env dev groups delete-all --log-dir Logs
```

**Note:** `delete-all` will skip groups listed in `PROTECTED_GROUP_IDS` in your `.env` file.

## Application Management

### List Applications
```powershell
# List all applications (displays formatted list with label, ID, and status)
okta-manager --env dev apps list

# Save to JSON
okta-manager --env dev apps list --output apps.json
```

**Output format:**
```
Found 7 applications

  My Application                            0oa21xdyzhwikdX280h8      ACTIVE
  Test App                                  0oa22tx82jcE9a4wT0h8      INACTIVE
  ...
```

### Delete Applications
```powershell
# Delete single application (requires confirmation)
okta-manager --env dev apps delete APP_ID

# Delete ALL applications except protected ones (requires confirmation)
okta-manager --env dev apps delete-all --log-dir Logs
```

**Note:** `delete-all` will skip applications listed in `PROTECTED_APP_IDS` in your `.env` file.

## Bulk Cleanup

### Full Cleanup
```powershell
# Clean up all resources (with confirmation)
okta-manager --env dev cleanup

# Skip specific resource types
okta-manager --env dev cleanup --skip-apps
okta-manager --env dev cleanup --skip-groups
okta-manager --env dev cleanup --skip-users
```

**Note:** Protected resources (defined in `.env`) will be automatically skipped.

## Getting Help

```powershell
# General help
okta-manager --help

# Command-specific help
okta-manager --env dev list-all --help
okta-manager --env dev users --help
okta-manager --env dev groups --help
okta-manager --env dev apps --help
okta-manager --env dev cleanup --help
```
