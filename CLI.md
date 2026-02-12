# AftershipStorage CLI

Unified command-line interface for all AfterDark Systems services.

## Installation

```bash
pip install -e .
```

This installs the `aftership` command.

## Quick Start

1. Initialize configuration:

```bash
aftership config init
```

2. Edit `aftership.yaml` and add your API keys

3. Use the CLI:

```bash
aftership darkship get /v1/shipments
aftership darkstorage get /v1/buckets
aftership aiserve get /v1/compute/jobs
```

## Configuration

### Initialize Config File

```bash
# Create full config template
aftership config init

# Create minimal config
aftership config init --minimal

# Create at custom location
aftership config init --path ~/.config/aftership/config.yaml
```

### Show Current Configuration

```bash
aftership config show

# Use specific config file
aftership config show --config /path/to/config.yaml
```

## Service Commands

All services support `get`, `post`, `put`, `patch`, and `delete` commands.

### General Syntax

```bash
aftership <service> <command> <endpoint> [options]
```

### Common Options

- `--config PATH` - Use specific config file
- `--format FORMAT` - Output format: json, yaml, table (default: json)
- `--data JSON` - JSON data for POST/PUT/PATCH requests

## Examples

### Darkship (Shipping Operations)

```bash
# List all shipments
aftership darkship get /v1/shipments

# Get specific shipment
aftership darkship get /v1/shipments/TRACK123

# Create new shipment
aftership darkship post /v1/shipments --data '{
  "tracking_number": "SHIP123",
  "carrier": "FedEx",
  "origin": {"city": "San Francisco"},
  "destination": {"city": "New York"}
}'

# Output as table
aftership darkship get /v1/shipments --format table
```

### Darkstorage (S3-Compatible Storage)

```bash
# List buckets
aftership darkstorage get /v1/buckets

# Create bucket
aftership darkstorage post /v1/buckets --data '{
  "name": "my-bucket",
  "region": "us-west-1"
}'

# List files in bucket
aftership darkstorage get /v1/buckets/my-bucket/objects

# Get upload URL
aftership darkstorage post /v1/upload --data '{
  "bucket": "my-bucket",
  "key": "file.txt"
}'
```

### Shipshack (Fleet Management)

```bash
# List all ships
aftership shipshack get /v1/ships

# Add new ship
aftership shipshack post /v1/ships --data '{
  "name": "Cargo Alpha",
  "type": "container",
  "capacity": 10000
}'

# Update ship location
aftership shipshack patch /v1/ships/123 --data '{
  "current_location": {
    "latitude": 40.7128,
    "longitude": -74.0060
  }
}'
```

### Models2go (Model Management)

```bash
# List published models
aftership models2go get /v1/models

# Publish new model
aftership models2go post /v1/models --data '{
  "name": "sentiment-analyzer",
  "version": "1.0.0",
  "framework": "pytorch",
  "file_url": "https://storage.example.com/model.pt"
}'

# Get model details
aftership models2go get /v1/models/model-id-123
```

### Hostscience (Hosting Infrastructure)

```bash
# List instances
aftership hostscience get /v1/instances

# Create new instance
aftership hostscience post /v1/instances --data '{
  "name": "web-server-01",
  "type": "compute",
  "plan": "standard",
  "region": "us-west-1"
}'

# Start instance
aftership hostscience post /v1/instances/inst-123/start

# Get instance metrics
aftership hostscience get /v1/instances/inst-123/metrics
```

### Aiserve (AI Compute)

```bash
# List compute resources
aftership aiserve get /v1/compute/resources

# Create training job
aftership aiserve post /v1/compute/jobs --data '{
  "name": "train-model",
  "type": "training",
  "gpu_type": "A100",
  "gpu_count": 4,
  "docker_image": "pytorch/pytorch:latest",
  "command": "python train.py"
}'

# Get job status
aftership aiserve get /v1/compute/jobs/job-123/status

# List inference endpoints
aftership aiserve get /v1/inference/endpoints

# Create inference endpoint
aftership aiserve post /v1/inference/endpoints --data '{
  "name": "my-api",
  "model_path": "https://storage/model.pt",
  "gpu_type": "T4"
}'
```

## Output Formats

### JSON (default)

```bash
aftership darkship get /v1/shipments --format json
```

### YAML

```bash
aftership darkship get /v1/shipments --format yaml
```

### Table

```bash
aftership darkship get /v1/shipments --format table
```

## Using Custom Config Files

```bash
# Use production config
aftership --config prod.yaml darkship get /v1/shipments

# Use staging config
aftership --config staging.yaml darkstorage get /v1/buckets
```

## Environment Variables

If no config file is found, the CLI falls back to environment variables:

```bash
export AFTERDARK_API_KEY=your-key
# or
export DARKSHIP_API_KEY=your-darkship-key
export DARKSTORAGE_API_KEY=your-darkstorage-key
# etc.

aftership darkship get /v1/shipments
```

## Error Handling

The CLI provides helpful error messages:

```bash
$ aftership darkship get /invalid
Error: 404 Not Found

$ aftership darkship get /v1/shipments
Error loading client: No config file found
Hint: Use 'aftership config init' to create a config file
```

## Shell Completion

Generate shell completion:

```bash
# Bash
_AFTERSHIP_COMPLETE=bash_source aftership > ~/.aftership-complete.bash
echo 'source ~/.aftership-complete.bash' >> ~/.bashrc

# Zsh
_AFTERSHIP_COMPLETE=zsh_source aftership > ~/.aftership-complete.zsh
echo 'source ~/.aftership-complete.zsh' >> ~/.zshrc

# Fish
_AFTERSHIP_COMPLETE=fish_source aftership > ~/.config/fish/completions/aftership.fish
```

## Tips

1. **Use aliases** for frequently accessed services:
   ```bash
   alias ads='aftership darkstorage'
   alias aai='aftership aiserve'
   ```

2. **Pipe output** to jq for advanced JSON processing:
   ```bash
   aftership darkship get /v1/shipments | jq '.[] | select(.status=="active")'
   ```

3. **Save responses** to files:
   ```bash
   aftership models2go get /v1/models > models.json
   ```

4. **Use environment-specific configs**:
   ```bash
   alias aftership-prod='aftership --config prod.yaml'
   alias aftership-staging='aftership --config staging.yaml'
   ```
