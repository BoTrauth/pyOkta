# Troubleshooting

## Common Issues

### Command Not Found: `okta-manager`

**Problem:** `okta-manager` is not recognized as a command.

**Solution:**
```powershell
# Ensure virtual environment is activated
.\.venv\Scripts\Activate.ps1

# Verify installation
uv pip list | Select-String "pyokta"
```

### Configuration Error: Missing Variables

**Problem:** `❌ Configuration error: Missing required environment variables`

**Solution:**
1. Ensure `.env` file exists:
   ```powershell
   Test-Path .env
   ```

2. If not, copy from template:
   ```powershell
   Copy-Item .env.example .env
   ```

3. Edit `.env` with valid credentials

### UV Not Found

**Problem:** `uv` command not recognized.

**Solution:**
```powershell
# Install uv
pip install uv

# Or use pip instead
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -e .
```

### Okta SDK Version Conflict

**Problem:** `KeyError: 'token'` or SDK compatibility issues.

**Solution:**
```powershell
# Ensure correct SDK version (2.9.x)
uv pip install "okta>=2.9.0,<3.0.0" --force-reinstall
```

### Permission Denied on .env

**Problem:** Cannot read `.env` file.

**Solution:**
```powershell
# Check file permissions
Get-Acl .env | Format-List

# Ensure file is readable
```

### Authentication Errors

**Problem:** `401 Unauthorized` or authentication failures.

**Solutions:**
1. Verify `OKTA_ORG_URL` is correct
2. Check `OKTA_CLIENT_ID` is valid
3. Ensure `OKTA_PRIVATE_KEY` JSON is properly formatted
4. Verify OAuth app has required scopes
5. Check API token hasn't expired

### Import Errors

**Problem:** `ModuleNotFoundError: No module named 'pyokta_manager'`

**Solution:**
```powershell
# Reinstall in editable mode
uv pip install -e .
```

### Async Runtime Errors

**Problem:** `RuntimeError: Event loop is closed`

**Solution:**
This is handled automatically by the CLI. If using programmatically:
```python
import asyncio
from pyokta_manager.client import OktaClientWrapper

async def main():
    # Your code here
    pass

asyncio.run(main())
```

## Debugging

### Enable Verbose Output

```powershell
# Check configuration
okta-manager --help

# Test with simple command
okta-manager users list
```

### Verify Environment

```powershell
# Check Python version (should be >=3.9)
python --version

# Check package installation
uv pip list

# Check .env file
Get-Content .env
```

### Test Okta Connection

```powershell
# Try listing users (simplest test)
okta-manager users list --status ACTIVE
```

## Getting Help

### Command Help
```powershell
# General help
okta-manager --help

# Command-specific help
okta-manager users --help
okta-manager groups --help
okta-manager apps --help
```

### Error Messages

Most error messages include helpful context:
- Missing configuration → Points to `.env.example`
- Permission issues → Shows what's protected
- API errors → Shows response details

## Support

For issues not covered here:
1. Check the full documentation in `README.md`
2. Review configuration in `.env`
3. Verify Okta API credentials in Okta admin console
