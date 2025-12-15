# Documentation

## Guides
- **[Installation](installation.md)** - Setup and install
- **[Usage](usage.md)** - All CLI commands
- **[Configuration](configuration.md)** - Environment variables
- **[Migration](migration.md)** - Old scripts → New CLI
- **[API Reference](api-reference.md)** - Package API
- **[Troubleshooting](troubleshooting.md)** - Common issues

## Quick Start
```powershell
uv venv && .\.venv\Scripts\Activate.ps1 && uv pip install -e .
Copy-Item .env.example .env  # Edit with your credentials
okta-manager users list
```
