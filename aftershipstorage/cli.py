"""Command-line interface for AftershipStorage."""
import sys
import json
import click
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.table import Table
from rich.json import JSON
from rich import print_json

from .client import AftershipStorage
from .config import Config


console = Console()


def load_client(config_path: Optional[str]) -> AftershipStorage:
    """Load AftershipStorage client from config or environment."""
    try:
        if config_path:
            return AftershipStorage.from_config(config_path)
        else:
            # Try config file first, fall back to env
            try:
                return AftershipStorage.from_config()
            except ValueError:
                return AftershipStorage.from_env()
    except Exception as e:
        console.print(f"[red]Error loading client: {e}[/red]")
        console.print("[yellow]Hint: Use 'aftership config init' to create a config file[/yellow]")
        sys.exit(1)


def format_output(data, output_format: str = "json"):
    """Format and print output."""
    if output_format == "json":
        print_json(data=data)
    elif output_format == "yaml":
        import yaml
        console.print(yaml.dump(data, default_flow_style=False))
    elif output_format == "table":
        if isinstance(data, list) and data:
            table = Table(show_header=True)
            # Add columns from first item keys
            for key in data[0].keys():
                table.add_column(str(key))
            # Add rows
            for item in data:
                table.add_row(*[str(v) for v in item.values()])
            console.print(table)
        else:
            print_json(data=data)
    else:
        console.print(data)


@click.group()
@click.version_option(version="0.1.0", prog_name="aftership")
def main():
    """AftershipStorage - Unified CLI for aftership services."""
    pass


@main.group()
def config():
    """Manage configuration."""
    pass


@config.command("init")
@click.option("--path", default="aftership.yaml", help="Config file path")
@click.option("--minimal", is_flag=True, help="Create minimal config")
def config_init(path: str, minimal: bool):
    """Initialize a new configuration file."""
    config_path = Path(path)

    if config_path.exists():
        if not click.confirm(f"Config file {path} already exists. Overwrite?"):
            return

    if minimal:
        config_content = """# AftershipStorage Configuration
afterdark_account:
  api_key: your-afterdark-api-key

settings:
  timeout: 30
  verify_ssl: true
"""
    else:
        config_content = """# AftershipStorage Configuration
afterdark_account:
  username: your-username
  api_key: your-afterdark-api-key
  account_id: your-account-id

# Individual service overrides (optional)
# darkship:
#   api_key: service-specific-key
#   base_url: https://api.darkship.io

# darkstorage:
#   api_key: service-specific-key
#   base_url: https://api.darkstorage.io

# shipshack:
#   api_key: service-specific-key
#   base_url: https://api.shipshack.io

# models2go:
#   api_key: service-specific-key
#   base_url: https://api.models2go.com

# hostscience:
#   api_key: service-specific-key
#   base_url: https://api.hostscience.io

# aiserve:
#   api_key: service-specific-key
#   base_url: https://api.aiserve.farm

settings:
  timeout: 30
  verify_ssl: true
"""

    config_path.write_text(config_content)
    console.print(f"[green]Created config file: {path}[/green]")
    console.print(f"[yellow]Edit {path} and add your API keys[/yellow]")


@config.command("show")
@click.option("--config", help="Config file path")
def config_show(config: Optional[str]):
    """Show current configuration."""
    try:
        if config:
            cfg = Config.from_file(config)
        else:
            cfg = Config.from_default_locations()
            if cfg is None:
                console.print("[yellow]No config file found[/yellow]")
                return

        print_json(data=cfg.to_dict())
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")


@main.group()
@click.option("--config", help="Config file path")
@click.pass_context
def darkship(ctx, config: Optional[str]):
    """Darkship.io - Shipping operations."""
    ctx.ensure_object(dict)
    ctx.obj["client"] = load_client(config)


@darkship.command("get")
@click.argument("endpoint")
@click.option("--format", "output_format", type=click.Choice(["json", "yaml", "table"]), default="json")
@click.pass_context
def darkship_get(ctx, endpoint: str, output_format: str):
    """Make a GET request to darkship.io."""
    client = ctx.obj["client"]
    response = client.darkship.get(endpoint)
    format_output(response.json(), output_format)


@darkship.command("post")
@click.argument("endpoint")
@click.option("--data", help="JSON data to send")
@click.option("--format", "output_format", type=click.Choice(["json", "yaml", "table"]), default="json")
@click.pass_context
def darkship_post(ctx, endpoint: str, data: Optional[str], output_format: str):
    """Make a POST request to darkship.io."""
    client = ctx.obj["client"]
    json_data = json.loads(data) if data else {}
    response = client.darkship.post(endpoint, json=json_data)
    format_output(response.json(), output_format)


@main.group()
@click.option("--config", help="Config file path")
@click.pass_context
def darkstorage(ctx, config: Optional[str]):
    """Darkstorage.io - S3-compatible storage."""
    ctx.ensure_object(dict)
    ctx.obj["client"] = load_client(config)


@darkstorage.command("get")
@click.argument("endpoint")
@click.option("--format", "output_format", type=click.Choice(["json", "yaml", "table"]), default="json")
@click.pass_context
def darkstorage_get(ctx, endpoint: str, output_format: str):
    """Make a GET request to darkstorage.io."""
    client = ctx.obj["client"]
    response = client.darkstorage.get(endpoint)
    format_output(response.json(), output_format)


@darkstorage.command("post")
@click.argument("endpoint")
@click.option("--data", help="JSON data to send")
@click.option("--format", "output_format", type=click.Choice(["json", "yaml", "table"]), default="json")
@click.pass_context
def darkstorage_post(ctx, endpoint: str, data: Optional[str], output_format: str):
    """Make a POST request to darkstorage.io."""
    client = ctx.obj["client"]
    json_data = json.loads(data) if data else {}
    response = client.darkstorage.post(endpoint, json=json_data)
    format_output(response.json(), output_format)


@main.group()
@click.option("--config", help="Config file path")
@click.pass_context
def shipshack(ctx, config: Optional[str]):
    """Shipshack.io - Fleet management."""
    ctx.ensure_object(dict)
    ctx.obj["client"] = load_client(config)


@shipshack.command("get")
@click.argument("endpoint")
@click.option("--format", "output_format", type=click.Choice(["json", "yaml", "table"]), default="json")
@click.pass_context
def shipshack_get(ctx, endpoint: str, output_format: str):
    """Make a GET request to shipshack.io."""
    client = ctx.obj["client"]
    response = client.shipshack.get(endpoint)
    format_output(response.json(), output_format)


@shipshack.command("post")
@click.argument("endpoint")
@click.option("--data", help="JSON data to send")
@click.option("--format", "output_format", type=click.Choice(["json", "yaml", "table"]), default="json")
@click.pass_context
def shipshack_post(ctx, endpoint: str, data: Optional[str], output_format: str):
    """Make a POST request to shipshack.io."""
    client = ctx.obj["client"]
    json_data = json.loads(data) if data else {}
    response = client.shipshack.post(endpoint, json=json_data)
    format_output(response.json(), output_format)


@main.group()
@click.option("--config", help="Config file path")
@click.pass_context
def models2go(ctx, config: Optional[str]):
    """Models2go.com - Model publishing and management."""
    ctx.ensure_object(dict)
    ctx.obj["client"] = load_client(config)


@models2go.command("get")
@click.argument("endpoint")
@click.option("--format", "output_format", type=click.Choice(["json", "yaml", "table"]), default="json")
@click.pass_context
def models2go_get(ctx, endpoint: str, output_format: str):
    """Make a GET request to models2go.com."""
    client = ctx.obj["client"]
    response = client.models2go.get(endpoint)
    format_output(response.json(), output_format)


@models2go.command("post")
@click.argument("endpoint")
@click.option("--data", help="JSON data to send")
@click.option("--format", "output_format", type=click.Choice(["json", "yaml", "table"]), default="json")
@click.pass_context
def models2go_post(ctx, endpoint: str, data: Optional[str], output_format: str):
    """Make a POST request to models2go.com."""
    client = ctx.obj["client"]
    json_data = json.loads(data) if data else {}
    response = client.models2go.post(endpoint, json=json_data)
    format_output(response.json(), output_format)


@main.group()
@click.option("--config", help="Config file path")
@click.pass_context
def hostscience(ctx, config: Optional[str]):
    """Hostscience.io - Hosting infrastructure."""
    ctx.ensure_object(dict)
    ctx.obj["client"] = load_client(config)


@hostscience.command("get")
@click.argument("endpoint")
@click.option("--format", "output_format", type=click.Choice(["json", "yaml", "table"]), default="json")
@click.pass_context
def hostscience_get(ctx, endpoint: str, output_format: str):
    """Make a GET request to hostscience.io."""
    client = ctx.obj["client"]
    response = client.hostscience.get(endpoint)
    format_output(response.json(), output_format)


@hostscience.command("post")
@click.argument("endpoint")
@click.option("--data", help="JSON data to send")
@click.option("--format", "output_format", type=click.Choice(["json", "yaml", "table"]), default="json")
@click.pass_context
def hostscience_post(ctx, endpoint: str, data: Optional[str], output_format: str):
    """Make a POST request to hostscience.io."""
    client = ctx.obj["client"]
    json_data = json.loads(data) if data else {}
    response = client.hostscience.post(endpoint, json=json_data)
    format_output(response.json(), output_format)


@main.group()
@click.option("--config", help="Config file path")
@click.pass_context
def aiserve(ctx, config: Optional[str]):
    """Aiserve.farm - AI compute management."""
    ctx.ensure_object(dict)
    ctx.obj["client"] = load_client(config)


@aiserve.command("get")
@click.argument("endpoint")
@click.option("--format", "output_format", type=click.Choice(["json", "yaml", "table"]), default="json")
@click.pass_context
def aiserve_get(ctx, endpoint: str, output_format: str):
    """Make a GET request to aiserve.farm."""
    client = ctx.obj["client"]
    response = client.aiserve.get(endpoint)
    format_output(response.json(), output_format)


@aiserve.command("post")
@click.argument("endpoint")
@click.option("--data", help="JSON data to send")
@click.option("--format", "output_format", type=click.Choice(["json", "yaml", "table"]), default="json")
@click.pass_context
def aiserve_post(ctx, endpoint: str, data: Optional[str], output_format: str):
    """Make a POST request to aiserve.farm."""
    client = ctx.obj["client"]
    json_data = json.loads(data) if data else {}
    response = client.aiserve.post(endpoint, json=json_data)
    format_output(response.json(), output_format)


if __name__ == "__main__":
    main()
