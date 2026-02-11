"""Main AftershipStorage meta client."""
import os
from typing import Optional
from dotenv import load_dotenv

from .services import (
    DarkshipClient,
    DarkstorageClient,
    ShipshackClient,
    Models2GoClient,
    HostscienceClient,
    AiserveClient
)


class AftershipStorage:
    """
    Meta client for managing multiple aftership storage services.

    Supports:
    - darkship.io
    - darkstorage.io
    - shipshack.io
    - models2go.com
    - hostscience.io
    - aiserve.farm
    """

    def __init__(
        self,
        darkship_api_key: Optional[str] = None,
        darkstorage_api_key: Optional[str] = None,
        shipshack_api_key: Optional[str] = None,
        models2go_api_key: Optional[str] = None,
        hostscience_api_key: Optional[str] = None,
        aiserve_api_key: Optional[str] = None,
        darkship_base_url: Optional[str] = None,
        darkstorage_base_url: Optional[str] = None,
        shipshack_base_url: Optional[str] = None,
        models2go_base_url: Optional[str] = None,
        hostscience_base_url: Optional[str] = None,
        aiserve_base_url: Optional[str] = None,
    ):
        """
        Initialize AftershipStorage meta client.

        Args:
            darkship_api_key: API key for darkship.io
            darkstorage_api_key: API key for darkstorage.io
            shipshack_api_key: API key for shipshack.io
            models2go_api_key: API key for models2go.com
            hostscience_api_key: API key for hostscience.io
            aiserve_api_key: API key for aiserve.farm
            darkship_base_url: Optional custom base URL for darkship.io
            darkstorage_base_url: Optional custom base URL for darkstorage.io
            shipshack_base_url: Optional custom base URL for shipshack.io
            models2go_base_url: Optional custom base URL for models2go.com
            hostscience_base_url: Optional custom base URL for hostscience.io
            aiserve_base_url: Optional custom base URL for aiserve.farm
        """
        # Initialize clients only if API keys are provided
        self._darkship = None
        self._darkstorage = None
        self._shipshack = None
        self._models2go = None
        self._hostscience = None
        self._aiserve = None

        if darkship_api_key:
            kwargs = {"api_key": darkship_api_key}
            if darkship_base_url:
                kwargs["base_url"] = darkship_base_url
            self._darkship = DarkshipClient(**kwargs)

        if darkstorage_api_key:
            kwargs = {"api_key": darkstorage_api_key}
            if darkstorage_base_url:
                kwargs["base_url"] = darkstorage_base_url
            self._darkstorage = DarkstorageClient(**kwargs)

        if shipshack_api_key:
            kwargs = {"api_key": shipshack_api_key}
            if shipshack_base_url:
                kwargs["base_url"] = shipshack_base_url
            self._shipshack = ShipshackClient(**kwargs)

        if models2go_api_key:
            kwargs = {"api_key": models2go_api_key}
            if models2go_base_url:
                kwargs["base_url"] = models2go_base_url
            self._models2go = Models2GoClient(**kwargs)

        if hostscience_api_key:
            kwargs = {"api_key": hostscience_api_key}
            if hostscience_base_url:
                kwargs["base_url"] = hostscience_base_url
            self._hostscience = HostscienceClient(**kwargs)

        if aiserve_api_key:
            kwargs = {"api_key": aiserve_api_key}
            if aiserve_base_url:
                kwargs["base_url"] = aiserve_base_url
            self._aiserve = AiserveClient(**kwargs)

    @classmethod
    def from_env(cls, env_file: Optional[str] = None):
        """
        Create client from environment variables.

        Looks for:
        - DARKSHIP_API_KEY
        - DARKSTORAGE_API_KEY
        - SHIPSHACK_API_KEY
        - MODELS2GO_API_KEY
        - HOSTSCIENCE_API_KEY
        - AISERVE_API_KEY

        Optional custom base URLs:
        - DARKSHIP_BASE_URL
        - DARKSTORAGE_BASE_URL
        - SHIPSHACK_BASE_URL
        - MODELS2GO_BASE_URL
        - HOSTSCIENCE_BASE_URL
        - AISERVE_BASE_URL

        Args:
            env_file: Optional path to .env file (default: searches for .env)

        Returns:
            AftershipStorage instance
        """
        if env_file:
            load_dotenv(env_file)
        else:
            load_dotenv()

        return cls(
            darkship_api_key=os.getenv("DARKSHIP_API_KEY"),
            darkstorage_api_key=os.getenv("DARKSTORAGE_API_KEY"),
            shipshack_api_key=os.getenv("SHIPSHACK_API_KEY"),
            models2go_api_key=os.getenv("MODELS2GO_API_KEY"),
            hostscience_api_key=os.getenv("HOSTSCIENCE_API_KEY"),
            aiserve_api_key=os.getenv("AISERVE_API_KEY"),
            darkship_base_url=os.getenv("DARKSHIP_BASE_URL"),
            darkstorage_base_url=os.getenv("DARKSTORAGE_BASE_URL"),
            shipshack_base_url=os.getenv("SHIPSHACK_BASE_URL"),
            models2go_base_url=os.getenv("MODELS2GO_BASE_URL"),
            hostscience_base_url=os.getenv("HOSTSCIENCE_BASE_URL"),
            aiserve_base_url=os.getenv("AISERVE_BASE_URL"),
        )

    @property
    def darkship(self) -> DarkshipClient:
        """Get darkship.io client."""
        if self._darkship is None:
            raise ValueError(
                "Darkship client not initialized. Provide darkship_api_key during initialization."
            )
        return self._darkship

    @property
    def darkstorage(self) -> DarkstorageClient:
        """Get darkstorage.io client."""
        if self._darkstorage is None:
            raise ValueError(
                "Darkstorage client not initialized. Provide darkstorage_api_key during initialization."
            )
        return self._darkstorage

    @property
    def shipshack(self) -> ShipshackClient:
        """Get shipshack.io client."""
        if self._shipshack is None:
            raise ValueError(
                "Shipshack client not initialized. Provide shipshack_api_key during initialization."
            )
        return self._shipshack

    @property
    def models2go(self) -> Models2GoClient:
        """Get models2go.com client."""
        if self._models2go is None:
            raise ValueError(
                "Models2Go client not initialized. Provide models2go_api_key during initialization."
            )
        return self._models2go

    @property
    def hostscience(self) -> HostscienceClient:
        """Get hostscience.io client."""
        if self._hostscience is None:
            raise ValueError(
                "Hostscience client not initialized. Provide hostscience_api_key during initialization."
            )
        return self._hostscience

    @property
    def aiserve(self) -> AiserveClient:
        """Get aiserve.farm client."""
        if self._aiserve is None:
            raise ValueError(
                "Aiserve client not initialized. Provide aiserve_api_key during initialization."
            )
        return self._aiserve

    def close_all(self):
        """Close all active client sessions."""
        for client in [
            self._darkship,
            self._darkstorage,
            self._shipshack,
            self._models2go,
            self._hostscience,
            self._aiserve
        ]:
            if client:
                client.close()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close_all()
