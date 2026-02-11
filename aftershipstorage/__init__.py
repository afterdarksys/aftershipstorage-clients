"""AftershipStorage - Meta client for aftership storage services."""

from .client import AftershipStorage
from .services import (
    DarkshipClient,
    DarkstorageClient,
    ShipshackClient,
    Models2GoClient,
    HostscienceClient,
    AiserveClient
)
from .base import BaseClient
from .config import Config, ServiceConfig, AfterDarkAccount

__version__ = "0.1.0"

__all__ = [
    "AftershipStorage",
    "DarkshipClient",
    "DarkstorageClient",
    "ShipshackClient",
    "Models2GoClient",
    "HostscienceClient",
    "AiserveClient",
    "BaseClient",
    "Config",
    "ServiceConfig",
    "AfterDarkAccount",
]
