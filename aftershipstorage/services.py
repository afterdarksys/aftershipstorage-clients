"""Individual service clients for each platform."""
from .base import BaseClient


class DarkshipClient(BaseClient):
    """Client for darkship.io API."""

    def __init__(self, api_key: str, base_url: str = "https://api.darkship.io"):
        """Initialize Darkship client."""
        super().__init__(base_url=base_url, api_key=api_key)


class DarkstorageClient(BaseClient):
    """Client for darkstorage.io API."""

    def __init__(self, api_key: str, base_url: str = "https://api.darkstorage.io"):
        """Initialize Darkstorage client."""
        super().__init__(base_url=base_url, api_key=api_key)


class ShipshackClient(BaseClient):
    """Client for shipshack.io API."""

    def __init__(self, api_key: str, base_url: str = "https://api.shipshack.io"):
        """Initialize Shipshack client."""
        super().__init__(base_url=base_url, api_key=api_key)


class Models2GoClient(BaseClient):
    """Client for models2go.com API."""

    def __init__(self, api_key: str, base_url: str = "https://api.models2go.com"):
        """Initialize Models2Go client."""
        super().__init__(base_url=base_url, api_key=api_key)


class HostscienceClient(BaseClient):
    """Client for hostscience.io API."""

    def __init__(self, api_key: str, base_url: str = "https://api.hostscience.io"):
        """Initialize Hostscience client."""
        super().__init__(base_url=base_url, api_key=api_key)


class AiserveClient(BaseClient):
    """Client for aiserve.farm API."""

    def __init__(self, api_key: str, base_url: str = "https://api.aiserve.farm"):
        """Initialize Aiserve client."""
        super().__init__(base_url=base_url, api_key=api_key)
