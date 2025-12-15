# Usage Guide

## User Management

### List Users
```powershell
# List all users (displays formatted list with email, name, and status)
okta-manager users list

# Filter by status
okta-manager users list --status ACTIVE
okta-manager users list --status DEPROVISIONED

# Save to JSON
okta-manager users list --output users.json
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
okta-manager users export --output-dir Output
```

### Create User
```powershell
# Create user
okta-manager users create -f John -l Doe -e john@example.com

# Create and activate immediately
okta-manager users create -f Jane -l Smith -e jane@example.com --activate

# Create with password
okta-manager users create -f Bob -l Johnson -e bob@example.com -p SecurePass123
```

### Manage User Status
```powershell
# Activate user
okta-manager users activate USER_ID

# Activate without email
okta-manager users activate USER_ID --no-send-email

# Deactivate user
okta-manager users deactivate USER_ID
```

### Delete Users
```powershell
# Delete single user (requires confirmation)
okta-manager users delete USER_ID

# Delete all deprovisioned users (requires confirmation)
okta-manager users delete-deprovisioned --log-dir Logs

# Delete ALL users except protected ones (requires confirmation)
okta-manager users delete-all --log-dir Logs
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
okta-manager groups list

# Save to JSON
okta-manager groups list --output groups.json
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
okta-manager groups create -n "Engineering Team" -d "Engineering department"
```

### Delete Groups
```powershell
# Delete single group (requires confirmation)
okta-manager groups delete GROUP_ID

# Delete ALL groups except protected ones (requires confirmation)
okta-manager groups delete-all --log-dir Logs
### List Applications
```powershell
# List all applications (displays formatted list with label, ID, and status)
okta-manager apps list

# Save to JSON
okta-manager apps list --output apps.json
```

**Output format:**
```
Found 7 applications

  My Application                            0oa21xdyzhwikdX280h8      ACTIVE
  Test App                                  0oa22tx82jcE9a4wT0h8      INACTIVE
  ...
```
### Delete Group
### Delete Applications
```powershell
# Delete single application (requires confirmation)
okta-manager apps delete APP_ID

# Delete ALL applications except protected ones (requires confirmation)
okta-manager apps delete-all --log-dir Logs
```

**Note:** `delete-all` will skip applications listed in `PROTECTED_APP_IDS` in your `.env` file.
## Application Management

### List Applications
```powershell
# List all applications
okta-manager apps list

# Save to JSON
okta-manager apps list --output apps.json
```

### Delete Application
```powershell
okta-manager apps delete APP_ID
```

## Bulk Cleanup

### Full Cleanup
```powershell
# Clean up all resources (with confirmation)
okta-manager cleanup

# Skip specific resource types
okta-manager cleanup --skip-apps
okta-manager cleanup --skip-groups
okta-manager cleanup --skip-users
```

**Note:** Protected resources (defined in `.env`) will be automatically skipped.

## Getting Help

```powershell
# General help
okta-manager --help

# Command-specific help
okta-manager users --help
okta-manager groups --help
okta-manager apps --help
okta-manager cleanup --help
```
