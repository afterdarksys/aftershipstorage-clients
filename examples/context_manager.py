"""Example using context manager for automatic cleanup."""
from aftershipstorage import AftershipStorage

# Using context manager ensures sessions are properly closed
with AftershipStorage.from_env() as client:
    # Make API calls
    response = client.darkship.get("/v1/shipments")
    print("Shipments:", response.json())

    # Create a new storage entry
    storage_data = {
        "name": "Archive Storage",
        "capacity": 500,
        "location": "Warehouse A"
    }
    response = client.darkstorage.post("/v1/storage", json=storage_data)
    print("Created storage:", response.json())

    # Update a ship
    ship_updates = {
        "status": "active",
        "location": "dock-1"
    }
    response = client.shipshack.patch("/v1/ships/123", json=ship_updates)
    print("Updated ship:", response.json())

# Sessions are automatically closed when exiting the context
