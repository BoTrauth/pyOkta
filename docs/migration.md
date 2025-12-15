# Migration from Old Scripts

## Old Script Mapping

| Old Script | New CLI Command |
|-----------|----------------|
| `app.py` | `okta-manager groups list --output Output/groups.json` |
| `app2.py` | `okta-manager cleanup` |
| `GetOktaObjects.py` | `okta-manager users list` / `groups list` / `apps list` |
| `okta_users_by_status.py` | `okta-manager users export` |
| `avtivate_user.py` | `okta-manager users activate USER_ID` |
| `CreateOktaObjects.py` | `okta-manager users create` / `groups create` |
| `delete_deprovisioned_users.py` | `okta-manager users delete-deprovisioned` |
| `analyze_okta_users.py` | `okta-manager users list --output file.json` |

## Configuration Migration

### Old: Hardcoded in Scripts
```python
config = {
    'orgUrl': 'https://dev-520699.oktapreview.com',
    'clientId': '0oa25xglftsc8nNHv0h8',
    'privateKey': "{...}",
}
```

### New: Environment Variables
```env
OKTA_ORG_URL=https://dev-520699.oktapreview.com
OKTA_CLIENT_ID=0oa25xglftsc8nNHv0h8
OKTA_PRIVATE_KEY={...}
```

## Protected Resources Migration

### Old: In Code
```python
DAVES_EMAIL = "dave.brann@intergraph.com"
LST_APPLICATIONS_IDs_NOT_TO_DELETE = ["0oa21...", "0oa22..."]
LST_GROUPS_IDS_NOT_TO_DELETE = ['00ga8...', '00g1m...']
```

### New: In .env
```env
PROTECTED_USER_EMAILS=dave.brann@intergraph.com
PROTECTED_APP_IDS=0oa21...,0oa22...
PROTECTED_GROUP_IDS=00ga8...,00g1m...
```

## Example Conversions

### List All Users
**Old:**
```powershell
python GetOktaObjects.py
```

**New:**
```powershell
okta-manager users list
```

### Export Users by Status
**Old:**
```powershell
python okta_users_by_status.py
```

**New:**
```powershell
okta-manager users export
```

### Delete Deprovisioned Users
**Old:**
```powershell
python delete_deprovisioned_users.py
```

**New:**
```powershell
okta-manager users delete-deprovisioned
```

### Full Cleanup
**Old:**
```powershell
python app2.py
```

**New:**
```powershell
okta-manager cleanup
```

## Benefits of New Approach

✅ **Single CLI** - One command instead of 8 scripts  
✅ **Secure** - No hardcoded credentials  
✅ **Consistent** - Unified interface for all operations  
✅ **Safe** - Built-in confirmations and protections  
✅ **Documented** - Help text for every command  
✅ **Maintainable** - Proper package structure
