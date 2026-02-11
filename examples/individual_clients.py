"""Example using individual service clients directly."""
from aftershipstorage import DarkshipClient, DarkstorageClient

# Use individual clients if you only need one service
with DarkshipClient(api_key="your-api-key") as darkship:
    response = darkship.get("/v1/shipments")
    print("Shipments:", response.json())

# Or with custom base URL
with DarkstorageClient(
    api_key="your-api-key",
    base_url="https://custom.darkstorage.io"
) as darkstorage:
    response = darkstorage.get("/v1/storage")
    print("Storage:", response.json())

# Make multiple requests with the same client
darkship_client = DarkshipClient(api_key="your-api-key")
try:
    # List shipments
    response = darkship_client.get("/v1/shipments")
    shipments = response.json()

    # Get details for each shipment
    for shipment in shipments:
        response = darkship_client.get(f"/v1/shipments/{shipment['id']}")
        print("Shipment details:", response.json())

finally:
    darkship_client.close()
