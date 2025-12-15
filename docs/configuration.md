# Configuration Guide

## Environment Variables

All configuration is managed through the `.env` file in the project root.

### Required Variables

```env
# Okta Organization URL
OKTA_ORG_URL=https://your-org.okta.com

# OAuth 2.0 Client ID
OKTA_CLIENT_ID=0oa...

# Private Key (JSON format)
OKTA_PRIVATE_KEY={"d":"...","p":"...","kty":"RSA",...}
```

### Optional Variables

```env
# API Scopes (comma-separated)
OKTA_SCOPES=okta.users.manage,okta.groups.manage,okta.apps.manage

# Protected user emails (won't be deleted)
PROTECTED_USER_EMAILS=admin@example.com,service@example.com

# Protected application IDs (won't be deleted)
PROTECTED_APP_IDS=app_id_1,app_id_2,app_id_3

# Protected group IDs (won't be deleted)
PROTECTED_GROUP_IDS=group_id_1,group_id_2
```

## Protected Resources

Resources listed in the protection variables will be automatically skipped during:
- `okta-manager cleanup`
- `okta-manager users delete-deprovisioned`
- Any bulk deletion operations

### Example Protected Configuration

```env
PROTECTED_USER_EMAILS=admin@company.com,api-service@company.com
PROTECTED_APP_IDS=0oa21xdyzhwikdX280h8,0oa22tx82jcE9a4wT0h8
PROTECTED_GROUP_IDS=00ga8odrxaV0HtAb90h7,00g1m0nlnaby0URcX0h8
```

## Using Custom Environment File

```powershell
# Specify custom .env file location
okta-manager --env-file path/to/.env users list
```

## Security Best Practices

1. **Never commit `.env`** to version control (already in `.gitignore`)
2. **Restrict file permissions** on `.env`
3. **Use separate configs** for different environments (dev, staging, prod)
4. **Rotate credentials** regularly
5. **Use minimal required scopes**

## Validating Configuration

The tool automatically validates configuration on startup:

```powershell
# Test configuration
okta-manager users list
```

If configuration is invalid, you'll see:
```
❌ Configuration error: Missing required environment variables: ...
```
