"""Configuration management for AftershipStorage client."""
import os
import yaml
from pathlib import Path
from typing import Optional, Dict, Any
from dataclasses import dataclass, field


@dataclass
class ServiceConfig:
    """Configuration for a single service."""
    api_key: Optional[str] = None
    base_url: Optional[str] = None


@dataclass
class AfterDarkAccount:
    """AfterDark Systems account credentials."""
    username: Optional[str] = None
    password: Optional[str] = None
    api_key: Optional[str] = None
    account_id: Optional[str] = None


@dataclass
class Config:
    """Main configuration object."""
    # Individual service configurations
    darkship: ServiceConfig = field(default_factory=ServiceConfig)
    darkstorage: ServiceConfig = field(default_factory=ServiceConfig)
    shipshack: ServiceConfig = field(default_factory=ServiceConfig)
    models2go: ServiceConfig = field(default_factory=ServiceConfig)
    hostscience: ServiceConfig = field(default_factory=ServiceConfig)
    aiserve: ServiceConfig = field(default_factory=ServiceConfig)

    # Centralized AfterDark Systems account
    afterdark_account: Optional[AfterDarkAccount] = None

    # Global settings
    timeout: int = 30
    verify_ssl: bool = True

    @classmethod
    def from_file(cls, config_path: str) -> "Config":
        """
        Load configuration from a YAML file.

        Args:
            config_path: Path to the YAML config file

        Returns:
            Config object

        Raises:
            FileNotFoundError: If config file doesn't exist
            ValueError: If config file is invalid
        """
        path = Path(config_path).expanduser()

        if not path.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")

        with open(path, 'r') as f:
            data = yaml.safe_load(f)

        if not data:
            raise ValueError(f"Config file is empty: {config_path}")

        return cls.from_dict(data)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Config":
        """
        Create Config from dictionary.

        Args:
            data: Configuration dictionary

        Returns:
            Config object
        """
        config = cls()

        # Load service configurations
        services = ['darkship', 'darkstorage', 'shipshack', 'models2go', 'hostscience', 'aiserve']
        for service in services:
            if service in data:
                service_data = data[service]
                setattr(config, service, ServiceConfig(
                    api_key=service_data.get('api_key'),
                    base_url=service_data.get('base_url')
                ))

        # Load AfterDark Systems account
        if 'afterdark_account' in data:
            account_data = data['afterdark_account']
            config.afterdark_account = AfterDarkAccount(
                username=account_data.get('username'),
                password=account_data.get('password'),
                api_key=account_data.get('api_key'),
                account_id=account_data.get('account_id')
            )

        # Load global settings
        if 'settings' in data:
            settings = data['settings']
            config.timeout = settings.get('timeout', 30)
            config.verify_ssl = settings.get('verify_ssl', True)

        return config

    @classmethod
    def from_default_locations(cls) -> Optional["Config"]:
        """
        Try to load config from default locations.

        Searches in order:
        1. ./aftership.yaml
        2. ./aftership.yml
        3. ~/.aftership/config.yaml
        4. ~/.aftership/config.yml
        5. ~/.config/aftership/config.yaml
        6. ~/.config/aftership/config.yml

        Returns:
            Config object if found, None otherwise
        """
        search_paths = [
            Path.cwd() / "aftership.yaml",
            Path.cwd() / "aftership.yml",
            Path.home() / ".aftership" / "config.yaml",
            Path.home() / ".aftership" / "config.yml",
            Path.home() / ".config" / "aftership" / "config.yaml",
            Path.home() / ".config" / "aftership" / "config.yml",
        ]

        for path in search_paths:
            if path.exists():
                return cls.from_file(str(path))

        return None

    def resolve_api_key(self, service: str) -> Optional[str]:
        """
        Resolve API key for a service.

        Priority:
        1. Service-specific API key
        2. AfterDark account API key
        3. Environment variable

        Args:
            service: Service name (e.g., 'darkship')

        Returns:
            API key or None
        """
        # Check service-specific key
        service_config = getattr(self, service, None)
        if service_config and service_config.api_key:
            return service_config.api_key

        # Check AfterDark account key
        if self.afterdark_account and self.afterdark_account.api_key:
            return self.afterdark_account.api_key

        # Check environment variable
        env_var = f"{service.upper()}_API_KEY"
        return os.getenv(env_var)

    def resolve_base_url(self, service: str, default: str) -> str:
        """
        Resolve base URL for a service.

        Priority:
        1. Service-specific base URL
        2. Environment variable
        3. Default value

        Args:
            service: Service name (e.g., 'darkship')
            default: Default base URL

        Returns:
            Base URL
        """
        # Check service-specific URL
        service_config = getattr(self, service, None)
        if service_config and service_config.base_url:
            return service_config.base_url

        # Check environment variable
        env_var = f"{service.upper()}_BASE_URL"
        env_url = os.getenv(env_var)
        if env_url:
            return env_url

        return default

    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary."""
        result = {}

        # Services
        services = ['darkship', 'darkstorage', 'shipshack', 'models2go', 'hostscience', 'aiserve']
        for service in services:
            service_config = getattr(self, service)
            if service_config.api_key or service_config.base_url:
                result[service] = {}
                if service_config.api_key:
                    result[service]['api_key'] = service_config.api_key
                if service_config.base_url:
                    result[service]['base_url'] = service_config.base_url

        # AfterDark account
        if self.afterdark_account:
            result['afterdark_account'] = {}
            if self.afterdark_account.username:
                result['afterdark_account']['username'] = self.afterdark_account.username
            if self.afterdark_account.password:
                result['afterdark_account']['password'] = self.afterdark_account.password
            if self.afterdark_account.api_key:
                result['afterdark_account']['api_key'] = self.afterdark_account.api_key
            if self.afterdark_account.account_id:
                result['afterdark_account']['account_id'] = self.afterdark_account.account_id

        # Settings
        result['settings'] = {
            'timeout': self.timeout,
            'verify_ssl': self.verify_ssl
        }

        return result

    def to_yaml(self, output_path: str):
        """Save config to YAML file."""
        with open(output_path, 'w') as f:
            yaml.dump(self.to_dict(), f, default_flow_style=False, sort_keys=False)
