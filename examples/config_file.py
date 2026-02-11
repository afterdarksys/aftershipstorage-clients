"""Example: Using configuration files with AftershipStorage."""
from aftershipstorage import AftershipStorage, Config, AfterDarkAccount

# Method 1: Load from specific config file
client = AftershipStorage.from_config("path/to/aftership.yaml")

# Method 2: Auto-discover config from default locations
# Searches: ./aftership.yaml, ~/.aftership/config.yaml, ~/.config/aftership/config.yaml
try:
    client = AftershipStorage.from_config()
except ValueError as e:
    print(f"No config file found: {e}")

# Method 3: Load and inspect config before creating client
config = Config.from_file("aftership.yaml")
print(f"Timeout: {config.timeout}")
print(f"Verify SSL: {config.verify_ssl}")

if config.afterdark_account:
    print(f"Using AfterDark account: {config.afterdark_account.username}")

# Create client from config object
client = AftershipStorage.from_config("aftership.yaml")

# Method 4: Create config programmatically
config = Config()
config.afterdark_account = AfterDarkAccount(
    username="user@example.com",
    api_key="master-key-123"
)
config.timeout = 60

# Save config to file
config.to_yaml("my-config.yaml")

# Use the config
client = AftershipStorage.from_config("my-config.yaml")

# Make API calls as usual
response = client.darkship.get("/v1/shipments")
print(f"Shipments: {response.json()}")

client.close_all()

# Priority demonstration
# Config resolution priority (highest to lowest):
# 1. Service-specific API key in config file
# 2. AfterDark account API key in config file
# 3. Environment variable (DARKSHIP_API_KEY, etc.)

# Example with mixed configuration:
config_dict = {
    "afterdark_account": {
        "api_key": "master-key"  # Used for all services by default
    },
    "darkship": {
        "api_key": "darkship-specific-key"  # Overrides for darkship only
    },
    "darkstorage": {
        "base_url": "https://custom.darkstorage.io"  # Custom URL, uses master key
    }
}

config = Config.from_dict(config_dict)
client = AftershipStorage.from_config("aftership.yaml")

# darkship uses "darkship-specific-key"
# darkstorage uses "master-key" with custom URL
# all other services use "master-key" with default URLs
