"""Example: Complete pipeline using all services together."""
from aftershipstorage import AftershipStorage

client = AftershipStorage.from_env()

print("=== Full Pipeline Example ===\n")

# Step 1: Upload model files to storage
print("1. Uploading model files to storage...")
model_file = {
    "bucket": "ml-models",
    "key": "models/sentiment-analyzer-v2.pt",
    "content_type": "application/octet-stream"
}
response = client.darkstorage.post("/v1/upload", json=model_file)
upload_url = response.json()["upload_url"]
print(f"   Upload URL obtained: {upload_url}\n")

# Step 2: Publish model to models2go
print("2. Publishing model to models2go.com...")
model = {
    "name": "sentiment-analyzer",
    "version": "2.0.0",
    "description": "Production sentiment analysis model",
    "framework": "pytorch",
    "file_url": f"https://darkstorage.io/ml-models/models/sentiment-analyzer-v2.pt",
    "tags": ["nlp", "sentiment", "production"]
}
response = client.models2go.post("/v1/models", json=model)
published_model = response.json()
print(f"   Model published: {published_model['id']}\n")

# Step 3: Deploy model on hosting infrastructure
print("3. Deploying model on hostscience.io...")
instance = {
    "name": "ml-inference-server",
    "type": "compute",
    "plan": "gpu-enabled",
    "region": "us-west-1",
    "specs": {
        "cpu": 8,
        "memory": 32,
        "memory_unit": "GB",
        "gpu": "nvidia-t4"
    },
    "os": "ubuntu-22.04",
    "tags": ["ml", "inference", "production"]
}
response = client.hostscience.post("/v1/instances", json=instance)
deployed_instance = response.json()
print(f"   Instance deployed: {deployed_instance['id']}\n")

# Step 4: Create physical shipment for hardware
print("4. Creating shipment for hardware components...")
shipment = {
    "tracking_number": "HW-" + deployed_instance['id'][:8],
    "carrier": "FedEx",
    "origin": {
        "name": "Hardware Supplier",
        "city": "San Jose",
        "state": "CA",
        "zip": "95110",
        "country": "US"
    },
    "destination": {
        "name": "Data Center West",
        "city": "San Francisco",
        "state": "CA",
        "zip": "94105",
        "country": "US"
    },
    "packages": [{
        "weight": 50,
        "weight_unit": "lb",
        "description": "GPU Server Components"
    }]
}
response = client.darkship.post("/v1/shipments", json=shipment)
created_shipment = response.json()
print(f"   Shipment created: {created_shipment['tracking_number']}\n")

# Step 5: Assign to shipping fleet
print("5. Assigning to ship fleet...")
response = client.shipshack.get("/v1/ships", params={"status": "active", "limit": 1})
available_ships = response.json()

if available_ships:
    ship_id = available_ships[0]["id"]
    assignment = {
        "ship_id": ship_id,
        "shipment_ids": [created_shipment["id"]],
        "loading_date": "2026-02-12"
    }
    response = client.shipshack.post("/v1/assignments", json=assignment)
    print(f"   Assigned to ship: {ship_id}\n")
else:
    print("   No ships available, creating new ship entry...\n")

# Step 6: Monitor everything
print("6. Monitoring pipeline status...")

# Check storage
response = client.darkstorage.get("/v1/buckets/ml-models/objects")
storage_status = response.json()
print(f"   Storage: {len(storage_status)} files")

# Check model status
response = client.models2go.get(f"/v1/models/{published_model['id']}")
model_status = response.json()
print(f"   Model: {model_status['name']} v{model_status['version']}")

# Check hosting
response = client.hostscience.get(f"/v1/instances/{deployed_instance['id']}")
instance_status = response.json()
print(f"   Hosting: {instance_status['name']} - {instance_status['status']}")

# Check shipment
response = client.darkship.get(f"/v1/shipments/{created_shipment['tracking_number']}")
shipment_status = response.json()
print(f"   Shipment: {shipment_status['tracking_number']} - {shipment_status['status']}")

print("\n=== Pipeline Complete ===")

client.close_all()
