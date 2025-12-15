# Installation Guide

## Prerequisites

- Python 3.9 or higher
- [uv](https://github.com/astral-sh/uv) package manager (recommended) or pip

## Quick Install with UV

```powershell
# Navigate to project directory
cd pyOkta

# Create virtual environment
uv venv

# Activate environment
.\.venv\Scripts\Activate.ps1

# Install package
uv pip install -e .
```

## Install with Pip

```powershell
# Create virtual environment
python -m venv venv

# Activate environment
.\venv\Scripts\Activate.ps1

# Install package
pip install -e .
```

## Configuration

1. **Copy environment template:**
   ```powershell
   Copy-Item .env.example .env
   ```

2. **Edit `.env` with your credentials:**
   - `OKTA_ORG_URL` - Your Okta organization URL
   - `OKTA_CLIENT_ID` - OAuth 2.0 client ID
   - `OKTA_PRIVATE_KEY` - Private key JSON from Okta
   - `OKTA_SCOPES` - Required API scopes
   - `PROTECTED_USER_EMAILS` - Users to protect from deletion
   - `PROTECTED_APP_IDS` - Applications to protect
   - `PROTECTED_GROUP_IDS` - Groups to protect

3. **Verify installation:**
   ```powershell
   okta-manager --help
   ```

## Getting Okta Credentials

1. Sign in to Okta admin console
2. Go to **Applications** → **Applications**
3. Create **API Services** application
4. Configure **OAuth 2.0 with Private Key**
5. Grant scopes: `okta.users.manage`, `okta.groups.manage`, `okta.apps.manage`
6. Generate private key and copy JSON to `.env`
