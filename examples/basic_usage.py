"""Basic usage example for AftershipStorage client."""
from aftershipstorage import AftershipStorage

# Example 1: Initialize with explicit API keys
client = AftershipStorage(
    darkship_api_key="your-darkship-key",
    darkstorage_api_key="your-darkstorage-key",
    shipshack_api_key="your-shipshack-key",
    models2go_api_key="your-models2go-key",
    hostscience_api_key="your-hostscience-key"
)

# Example 2: Initialize from environment variables
client = AftershipStorage.from_env()

# Example 3: Initialize only specific services
client = AftershipStorage(
    darkship_api_key="your-darkship-key",
    darkstorage_api_key="your-darkstorage-key"
)

# Making requests to different services
try:
    # Darkship API call
    response = client.darkship.get("/v1/shipments")
    print("Darkship response:", response.json())

    # Darkstorage API call
    response = client.darkstorage.get("/v1/storage")
    print("Darkstorage response:", response.json())

    # Shipshack API call
    response = client.shipshack.post("/v1/ships", json={
        "name": "My Ship",
        "capacity": 1000
    })
    print("Shipshack response:", response.json())

    # Models2Go API call
    response = client.models2go.get("/v1/models")
    print("Models2Go response:", response.json())

    # Hostscience API call
    response = client.hostscience.get("/v1/hosts")
    print("Hostscience response:", response.json())

except Exception as e:
    print(f"Error: {e}")
finally:
    client.close_all()
