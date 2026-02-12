# AftershipStorage Meta Client

A unified Python client and CLI for interacting with multiple services in the aftership storage pipeline:

- **darkship.io** - Shipping operations
- **darkstorage.io** - Storage management (S3-compatible)
- **shipshack.io** - Ship fleet management
- **models2go.com** - Model publishing and management
- **hostscience.io** - Hosting infrastructure
- **aiserve.farm** - AI compute management

## Features

- **Unified Interface** - One client for all 6 services
- **Multiple Auth Methods** - Config file, environment variables, or direct instantiation
- **CLI Tool** - `aftership` command for terminal usage
- **Centralized Account** - Use single AfterDark Systems API key for all services
- **Service-Specific Overrides** - Custom keys or endpoints per service
- **Rich Output** - JSON, YAML, or formatted tables in CLI
- **Type-Safe** - Full Python type hints

## Documentation

- **[INSTALL.md](INSTALL.md)** - Complete installation guide
- **[CLI.md](CLI.md)** - CLI documentation and examples
- **[examples/](examples/)** - Python code examples

## Quick Install

```bash
pip install -e .
```

This installs both the Python library and the `aftership` CLI command.

For detailed installation instructions, see [INSTALL.md](INSTALL.md).

## Usage

The AftershipStorage client can be used in two ways:

1. **Python Library** - Import and use programmatically
2. **CLI Tool** - Use the `aftership` command from your terminal

### CLI Quick Start

```bash
# Initialize config
aftership config init

# Edit aftership.yaml with your API keys

# Use the CLI
aftership darkship get /v1/shipments
aftership darkstorage get /v1/buckets
aftership aiserve get /v1/compute/jobs
```

See [CLI.md](CLI.md) for complete CLI documentation.

## Python Library Usage

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

## Examples

Check the [examples/](examples/) directory for:

- **basic_usage.py** - Simple usage examples
- **config_file.py** - Configuration file examples
- **file_storage.py** - S3-compatible storage operations
- **model_management.py** - Model publishing workflow
- **product_shipping.py** - Shipping and fleet management
- **hosting_resources.py** - Infrastructure management
- **ai_compute.py** - AI training and inference
- **full_pipeline.py** - Complete end-to-end pipeline
- **cli_usage.sh** - CLI command examples

## Development

Install development dependencies:

```bash
pip install -e ".[dev]"
```

Run tests:

```bash
pytest
```

## Repository

- **GitHub**: https://github.com/afterdarksys/aftershipstorage-clients
- **Issues**: https://github.com/afterdarksys/aftershipstorage-clients/issues

## License

See LICENSE file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.
