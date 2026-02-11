"""Example: Product shipping operations via darkship.io and shipshack.io."""
from aftershipstorage import AftershipStorage

client = AftershipStorage.from_env()

# === DARKSHIP.IO - Shipping Management ===

# Create a new shipment
shipment = {
    "tracking_number": "SHIP123456",
    "carrier": "FedEx",
    "origin": {
        "name": "Warehouse A",
        "address": "123 Storage St",
        "city": "San Francisco",
        "state": "CA",
        "zip": "94105",
        "country": "US"
    },
    "destination": {
        "name": "John Doe",
        "address": "456 Delivery Ave",
        "city": "New York",
        "state": "NY",
        "zip": "10001",
        "country": "US"
    },
    "packages": [
        {
            "weight": 2.5,
            "weight_unit": "lb",
            "dimensions": {
                "length": 12,
                "width": 8,
                "height": 6,
                "unit": "in"
            }
        }
    ],
    "service_type": "standard"
}
response = client.darkship.post("/v1/shipments", json=shipment)
created_shipment = response.json()
print(f"Created shipment: {created_shipment}")

# Track a shipment
tracking_number = created_shipment["tracking_number"]
response = client.darkship.get(f"/v1/shipments/{tracking_number}")
tracking_info = response.json()
print(f"Tracking info: {tracking_info}")

# Get shipping rates
rate_request = {
    "origin_zip": "94105",
    "destination_zip": "10001",
    "weight": 2.5,
    "weight_unit": "lb",
    "dimensions": {
        "length": 12,
        "width": 8,
        "height": 6,
        "unit": "in"
    }
}
response = client.darkship.post("/v1/rates", json=rate_request)
rates = response.json()
print(f"Available rates: {rates}")

# Create a shipping label
label_request = {
    "shipment_id": created_shipment["id"],
    "format": "pdf"
}
response = client.darkship.post("/v1/labels", json=label_request)
label = response.json()
print(f"Label URL: {label['label_url']}")

# === SHIPSHACK.IO - Ship Fleet Management ===

# List all ships in fleet
response = client.shipshack.get("/v1/ships")
ships = response.json()
print(f"Ships in fleet: {ships}")

# Add a new ship to the fleet
new_ship = {
    "name": "Cargo Vessel Alpha",
    "type": "container",
    "capacity": 10000,
    "capacity_unit": "TEU",
    "status": "active",
    "current_location": {
        "latitude": 37.7749,
        "longitude": -122.4194,
        "port": "San Francisco"
    }
}
response = client.shipshack.post("/v1/ships", json=new_ship)
ship = response.json()
print(f"Added ship: {ship}")

# Update ship status and location
ship_id = ship["id"]
updates = {
    "status": "in-transit",
    "current_location": {
        "latitude": 40.7128,
        "longitude": -74.0060,
        "port": "New York"
    }
}
response = client.shipshack.patch(f"/v1/ships/{ship_id}", json=updates)
updated_ship = response.json()
print(f"Updated ship: {updated_ship}")

# Assign shipments to a ship
assignment = {
    "ship_id": ship_id,
    "shipment_ids": [created_shipment["id"]],
    "loading_date": "2026-02-15"
}
response = client.shipshack.post("/v1/assignments", json=assignment)
print(f"Assignment created: {response.json()}")

# Get ship capacity and utilization
response = client.shipshack.get(f"/v1/ships/{ship_id}/capacity")
capacity = response.json()
print(f"Ship capacity: {capacity}")

# Track ship route
response = client.shipshack.get(f"/v1/ships/{ship_id}/route")
route = response.json()
print(f"Ship route: {route}")

client.close_all()
