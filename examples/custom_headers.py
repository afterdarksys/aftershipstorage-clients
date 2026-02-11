"""Example with custom headers and request options."""
from aftershipstorage import AftershipStorage

client = AftershipStorage.from_env()

# Add custom headers to a request
custom_headers = {
    "X-Request-ID": "12345",
    "X-Custom-Header": "custom-value"
}

response = client.darkship.get(
    "/v1/shipments",
    headers=custom_headers
)
print("Response:", response.json())

# Use query parameters
params = {
    "status": "active",
    "limit": 10,
    "offset": 0
}

response = client.darkstorage.get(
    "/v1/storage",
    params=params
)
print("Filtered results:", response.json())

# Set timeout for long-running requests
response = client.models2go.get(
    "/v1/models/large-export",
    timeout=60  # 60 seconds timeout
)
print("Export:", response.json())

client.close_all()
