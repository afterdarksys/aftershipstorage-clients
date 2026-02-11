# AftershipStorage Meta Client

A unified Python client for interacting with multiple services in the aftership storage pipeline:

- **darkship.io** - Shipping operations
- **darkstorage.io** - Storage management (S3-compatible)
- **shipshack.io** - Ship fleet management
- **models2go.com** - Model publishing and management
- **hostscience.io** - Hosting infrastructure
- **aiserve.farm** - AI compute management

## Installation

```bash
pip install -e .
```

## Usage

### Basic Setup

```python
from aftershipstorage import AftershipStorage

# Initialize with API keys for each service
client = AftershipStorage(
    darkship_api_key="your-darkship-key",
    darkstorage_api_key="your-darkstorage-key",
    shipshack_api_key="your-shipshack-key",
    models2go_api_key="your-models2go-key",
    hostscience_api_key="your-hostscience-key",
    aiserve_api_key="your-aiserve-key"
)
```

### Using Environment Variables

Create a `.env` file:

```env
DARKSHIP_API_KEY=your-darkship-key
DARKSTORAGE_API_KEY=your-darkstorage-key
SHIPSHACK_API_KEY=your-shipshack-key
MODELS2GO_API_KEY=your-models2go-key
HOSTSCIENCE_API_KEY=your-hostscience-key
AISERVE_API_KEY=your-aiserve-key
```

Then initialize:

```python
from aftershipstorage import AftershipStorage

client = AftershipStorage.from_env()
```

### Using Configuration Files

Create a config file (`aftership.yaml`):

```yaml
# Option 1: Use centralized AfterDark Systems account
afterdark_account:
  username: your-username
  api_key: your-afterdark-api-key

# Option 2: Individual service configuration
darkship:
  api_key: your-darkship-key
  base_url: https://api.darkship.io  # Optional

darkstorage:
  api_key: your-darkstorage-key

# Add other services as needed...

settings:
  timeout: 30
  verify_ssl: true
```

Then initialize:

```python
from aftershipstorage import AftershipStorage

# Load from specific file
client = AftershipStorage.from_config("path/to/aftership.yaml")

# Or auto-discover from default locations:
# - ./aftership.yaml
# - ~/.aftership/config.yaml
# - ~/.config/aftership/config.yaml
client = AftershipStorage.from_config()
```

**Configuration Priority:**

1. Service-specific API key in config file
2. AfterDark account API key (applies to all services)
3. Environment variables

This allows you to use a single AfterDark Systems account API key for all services, or override specific services with their own keys.

### Access Individual Services

```python
# Access darkship.io
response = client.darkship.get("/endpoint")

# Access darkstorage.io
response = client.darkstorage.post("/endpoint", data={"key": "value"})

# Access shipshack.io
response = client.shipshack.get("/endpoint")

# Access models2go.com
response = client.models2go.get("/endpoint")

# Access hostscience.io
response = client.hostscience.get("/endpoint")

# Access aiserve.farm
response = client.aiserve.get("/endpoint")
```

## Development

Install development dependencies:

```bash
pip install -e ".[dev]"
```

Run tests:

```bash
pytest
```
