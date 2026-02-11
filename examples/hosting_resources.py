"""Example: Managing hosting resources via hostscience.io."""
from aftershipstorage import AftershipStorage

client = AftershipStorage.from_env()

# List all hosting resources
response = client.hostscience.get("/v1/resources")
resources = response.json()
print(f"Available resources: {resources}")

# Create a new hosting instance
new_instance = {
    "name": "web-server-01",
    "type": "compute",
    "plan": "standard",
    "region": "us-west-1",
    "specs": {
        "cpu": 4,
        "memory": 8,
        "memory_unit": "GB",
        "storage": 100,
        "storage_unit": "GB"
    },
    "os": "ubuntu-22.04",
    "tags": ["production", "web-server"]
}
response = client.hostscience.post("/v1/instances", json=new_instance)
instance = response.json()
print(f"Created instance: {instance}")

# Get instance details
instance_id = instance["id"]
response = client.hostscience.get(f"/v1/instances/{instance_id}")
details = response.json()
print(f"Instance details: {details}")

# Start/stop instance
response = client.hostscience.post(f"/v1/instances/{instance_id}/start")
print(f"Instance started: {response.json()}")

response = client.hostscience.post(f"/v1/instances/{instance_id}/stop")
print(f"Instance stopped: {response.json()}")

# Scale instance resources
scale_request = {
    "cpu": 8,
    "memory": 16,
    "memory_unit": "GB"
}
response = client.hostscience.patch(f"/v1/instances/{instance_id}/scale", json=scale_request)
scaled_instance = response.json()
print(f"Scaled instance: {scaled_instance}")

# Get instance metrics
response = client.hostscience.get(
    f"/v1/instances/{instance_id}/metrics",
    params={
        "metric": "cpu,memory,network",
        "period": "1h"
    }
)
metrics = response.json()
print(f"Instance metrics: {metrics}")

# Create a snapshot/backup
snapshot = {
    "instance_id": instance_id,
    "name": "backup-2026-02-11",
    "description": "Daily backup"
}
response = client.hostscience.post("/v1/snapshots", json=snapshot)
snapshot_info = response.json()
print(f"Created snapshot: {snapshot_info}")

# List snapshots
response = client.hostscience.get(
    "/v1/snapshots",
    params={"instance_id": instance_id}
)
snapshots = response.json()
print(f"Snapshots: {snapshots}")

# Restore from snapshot
restore_request = {
    "snapshot_id": snapshot_info["id"],
    "instance_id": instance_id
}
response = client.hostscience.post("/v1/restore", json=restore_request)
print(f"Restore initiated: {response.json()}")

# Manage DNS records
dns_record = {
    "domain": "example.com",
    "type": "A",
    "name": "web",
    "value": instance["public_ip"],
    "ttl": 3600
}
response = client.hostscience.post("/v1/dns/records", json=dns_record)
print(f"DNS record created: {response.json()}")

# List all DNS records
response = client.hostscience.get("/v1/dns/records", params={"domain": "example.com"})
dns_records = response.json()
print(f"DNS records: {dns_records}")

# Delete instance
response = client.hostscience.delete(f"/v1/instances/{instance_id}")
print(f"Instance deleted: {response.status_code == 204}")

client.close_all()
