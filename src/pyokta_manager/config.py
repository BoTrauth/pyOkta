"""Configuration management for Okta client."""

import os
from pathlib import Path
from typing import List, Optional

from dotenv import load_dotenv


class OktaConfig:
    """Manages Okta configuration from environment variables."""

    def __init__(self, env_file: Optional[str] = None, environment: Optional[str] = None):
        """
        Initialize Okta configuration.

        Args:
            env_file: Path to .env file. If None, searches for .env or .env.{environment} in project root.
            environment: Environment name (e.g., 'dev', 'qa', 'prev'). If provided, loads .env.{environment}.
        """
        if env_file:
            load_dotenv(env_file)
        else:
            # Search for .env or .env.{environment} in project root
            project_root = Path(__file__).parent.parent.parent
            
            if environment:
                env_path = project_root / f".env.{environment}"
                if not env_path.exists():
                    raise ValueError(
                        f"Environment file .env.{environment} not found.\n"
                        f"Available environments: dev, qa, prev"
                    )
            else:
                env_path = project_root / ".env"
                if not env_path.exists():
                    raise ValueError(
                        f".env file not found.\n"
                        f"Please create a .env file or specify an environment with --env"
                    )
            
            load_dotenv(env_path)

        self._validate_config()

    def _validate_config(self):
        """Validate required environment variables are set."""
        required = ["OKTA_ORG_URL", "OKTA_CLIENT_ID", "OKTA_PRIVATE_KEY"]
        missing = [var for var in required if not os.getenv(var)]
        if missing:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing)}\n"
                f"Please create a .env file based on .env.example"
            )

    @property
    def org_url(self) -> str:
        """Okta organization URL."""
        return os.getenv("OKTA_ORG_URL", "")

    @property
    def client_id(self) -> str:
        """OAuth 2.0 client ID."""
        return os.getenv("OKTA_CLIENT_ID", "")

    @property
    def private_key(self) -> str:
        """OAuth 2.0 private key (JSON string)."""
        return os.getenv("OKTA_PRIVATE_KEY", "")

    @property
    def scopes(self) -> List[str]:
        """OAuth 2.0 scopes."""
        scopes_str = os.getenv("OKTA_SCOPES", "okta.users.manage,okta.groups.manage,okta.apps.manage")
        return [s.strip() for s in scopes_str.split(",")]

    @property
    def protected_user_emails(self) -> List[str]:
        """List of user emails that should not be deleted."""
        emails_str = os.getenv("PROTECTED_USER_EMAILS", "")
        return [e.strip() for e in emails_str.split(",") if e.strip()]

    @property
    def protected_app_ids(self) -> List[str]:
        """List of application IDs that should not be deleted."""
        ids_str = os.getenv("PROTECTED_APP_IDS", "")
        return [i.strip() for i in ids_str.split(",") if i.strip()]

    @property
    def protected_group_ids(self) -> List[str]:
        """List of group IDs that should not be deleted."""
        ids_str = os.getenv("PROTECTED_GROUP_IDS", "")
        return [i.strip() for i in ids_str.split(",") if i.strip()]

    def get_client_config(self) -> dict:
        """
        Get configuration dict for Okta client.

        Returns:
            Dictionary with Okta client configuration.
        """
        return {
            "orgUrl": self.org_url,
            "authorizationMode": "PrivateKey",
            "clientId": self.client_id,
            "scopes": self.scopes,
            "privateKey": self.private_key,
        }
