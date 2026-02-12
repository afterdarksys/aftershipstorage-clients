# AftershipStorage Installation Guide

Complete installation guide for the AftershipStorage meta client.

## Requirements

- Python 3.8 or higher
- pip (Python package installer)

## Installation Methods

### Method 1: Install from Source (Recommended for Development)

```bash
# Clone the repository
git clone https://github.com/afterdarksys/aftershipstorage-clients.git
cd aftershipstorage-clients

# Install in development mode
pip install -e .

# Verify installation
aftership --version
```

### Method 2: Install from PyPI (When Published)

```bash
pip install aftershipstorage

# Verify installation
aftership --version
```

### Method 3: Install with Development Dependencies

```bash
# Clone and install with dev dependencies
git clone https://github.com/afterdarksys/aftershipstorage-clients.git
cd aftershipstorage-clients
pip install -e ".[dev]"
```

## Dependencies

The following packages will be automatically installed:

- `requests>=2.31.0` - HTTP client
- `python-dotenv>=1.0.0` - Environment variable management
- `pyyaml>=6.0.0` - YAML configuration support
- `click>=8.0.0` - CLI framework
- `rich>=13.0.0` - Terminal formatting

### Development Dependencies (Optional)

- `pytest>=7.0.0` - Testing framework
- `black>=23.0.0` - Code formatter
- `mypy>=1.0.0` - Type checker

## Post-Installation Configuration

### Option 1: Using Configuration File

1. Initialize a configuration file:
   ```bash
   aftership config init
   ```

2. Edit the generated `aftership.yaml`:
   ```yaml
   afterdark_account:
     api_key: your-afterdark-api-key

   settings:
     timeout: 30
     verify_ssl: true
   ```

3. Test the configuration:
   ```bash
   aftership config show
   ```

### Option 2: Using Environment Variables

Create a `.env` file in your project directory:

```env
AFTERDARK_API_KEY=your-afterdark-api-key
# Or individual service keys:
DARKSHIP_API_KEY=your-darkship-key
DARKSTORAGE_API_KEY=your-darkstorage-key
SHIPSHACK_API_KEY=your-shipshack-key
MODELS2GO_API_KEY=your-models2go-key
HOSTSCIENCE_API_KEY=your-hostscience-key
AISERVE_API_KEY=your-aiserve-key
```

### Option 3: System-Wide Configuration

For system-wide configuration, place your config file in one of these locations:

```bash
# Linux/macOS
mkdir -p ~/.config/aftership
cp aftership.yaml ~/.config/aftership/config.yaml

# Alternative location
mkdir -p ~/.aftership
cp aftership.yaml ~/.aftership/config.yaml
```

## Verification

Test your installation:

```bash
# Check version
aftership --version

# Test configuration
aftership config show

# Test API connectivity (requires valid API keys)
aftership darkship get /v1/health
```

## Upgrading

### From Source

```bash
cd aftershipstorage-clients
git pull
pip install -e . --upgrade
```

### From PyPI (When Published)

```bash
pip install --upgrade aftershipstorage
```

## Uninstallation

```bash
pip uninstall aftershipstorage
```

Remove configuration files:

```bash
rm -rf ~/.aftership
rm -rf ~/.config/aftership
rm aftership.yaml aftership.yml
```

## Virtual Environment Setup (Recommended)

Using a virtual environment is recommended to avoid dependency conflicts:

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install aftershipstorage
pip install -e .

# When done, deactivate
deactivate
```

## Docker Installation (Optional)

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Clone and install
RUN apt-get update && apt-get install -y git
RUN git clone https://github.com/afterdarksys/aftershipstorage-clients.git
WORKDIR /app/aftershipstorage-clients
RUN pip install -e .

# Copy your config
COPY aftership.yaml /root/.aftership/config.yaml

# Set entrypoint
ENTRYPOINT ["aftership"]
```

Build and run:

```bash
docker build -t aftership .
docker run aftership config show
docker run aftership darkship get /v1/shipments
```

## Troubleshooting

### "command not found: aftership"

The installation didn't complete successfully. Try:

```bash
pip install -e . --force-reinstall
```

Ensure your Python scripts directory is in PATH:

```bash
# Add to ~/.bashrc or ~/.zshrc
export PATH="$HOME/.local/bin:$PATH"
```

### "No module named 'aftershipstorage'"

The package isn't installed. Run:

```bash
pip install -e .
```

### "No config file found"

Create a config file:

```bash
aftership config init
```

Or use environment variables instead.

### Import Errors

Ensure all dependencies are installed:

```bash
pip install -r requirements.txt
```

Or reinstall:

```bash
pip install -e . --force-reinstall
```

### SSL Certificate Errors

If you encounter SSL errors, you can disable SSL verification (not recommended for production):

```yaml
# In aftership.yaml
settings:
  verify_ssl: false
```

## Platform-Specific Notes

### macOS

If you get SSL certificate errors on macOS:

```bash
/Applications/Python\ 3.x/Install\ Certificates.command
```

### Windows

On Windows, use PowerShell or Command Prompt:

```powershell
# Activate virtual environment
venv\Scripts\activate

# Install
pip install -e .
```

### Linux

Some distributions may require additional packages:

```bash
# Ubuntu/Debian
sudo apt-get install python3-dev python3-pip

# CentOS/RHEL
sudo yum install python3-devel
```

## Getting API Keys

To use AftershipStorage, you need API keys from AfterDark Systems:

1. Visit https://afterdarksystems.com (or your organization's portal)
2. Log in or create an account
3. Navigate to API Keys section
4. Generate a master API key or individual service keys
5. Add keys to your configuration file or environment variables

## Next Steps

After installation:

1. Read [README.md](README.md) for usage examples
2. Read [CLI.md](CLI.md) for CLI documentation
3. Explore [examples/](examples/) directory for code samples
4. Configure your API keys
5. Start using AftershipStorage!

## Support

- GitHub Issues: https://github.com/afterdarksys/aftershipstorage-clients/issues
- Documentation: See README.md and CLI.md
- Examples: See examples/ directory
