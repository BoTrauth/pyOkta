"""Okta client wrapper and utilities."""

from typing import List, Tuple

from okta.client import Client as OktaClient

from .config import OktaConfig


class OktaClientWrapper:
    """Wrapper around Okta SDK client with helper methods."""

    def __init__(self, config: OktaConfig):
        """
        Initialize Okta client wrapper.

        Args:
            config: OktaConfig instance.
        """
        self.config = config
        self.client = OktaClient(config.get_client_config())

    async def get_all_users(self, query_params: dict = None) -> List:
        """
        Retrieve all users with automatic pagination.

        Args:
            query_params: Optional query parameters for filtering.

        Returns:
            List of all users.
        """
        all_users = []
        users, resp, err = await self.client.list_users(query_params=query_params)
        if err:
            print(f"Error fetching users: {err}")
            return all_users

        all_users.extend(users)
        while resp.has_next():
            users, err = await resp.next()
            if err:
                print(f"Error fetching next page: {err}")
                break
            all_users.extend(users)

        return all_users

    async def get_all_groups(self) -> List:
        """
        Retrieve all groups with automatic pagination.

        Returns:
            List of all groups.
        """
        all_groups = []
        groups, resp, err = await self.client.list_groups()
        if err:
            print(f"Error listing groups: {err}")
            return all_groups

        all_groups.extend(groups)
        while resp.has_next():
            groups, err = await resp.next()
            if err:
                print(f"Error fetching next page of groups: {err}")
                break
            all_groups.extend(groups)

        return all_groups

    async def get_all_applications(self) -> List:
        """
        Retrieve all applications with automatic pagination.

        Returns:
            List of all applications.
        """
        all_apps = []
        apps, resp, err = await self.client.list_applications()
        if err:
            print(f"Error listing applications: {err}")
            return all_apps

        all_apps.extend(apps)
        while resp.has_next():
            apps, err = await resp.next()
            if err:
                print(f"Error fetching next page of applications: {err}")
                break
            all_apps.extend(apps)

        return all_apps

    def is_protected_user(self, user) -> bool:
        """Check if user is protected from deletion."""
        email = getattr(user.profile, "email", "")
        login = getattr(user.profile, "login", "")
        protected = self.config.protected_user_emails
        return email in protected or login in protected

    def is_protected_app(self, app_id: str) -> bool:
        """Check if application is protected from deletion."""
        return app_id in self.config.protected_app_ids

    def is_protected_group(self, group_id: str) -> bool:
        """Check if group is protected from deletion."""
        return group_id in self.config.protected_group_ids
