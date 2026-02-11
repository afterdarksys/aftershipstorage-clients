"""Example: File storage operations using darkstorage.io (S3-compatible)."""
from aftershipstorage import AftershipStorage

client = AftershipStorage.from_env()

# List all buckets/storage locations
response = client.darkstorage.get("/v1/buckets")
buckets = response.json()
print(f"Available buckets: {buckets}")

# Create a new bucket
new_bucket = {
    "name": "my-app-data",
    "region": "us-west-1",
    "acl": "private"
}
response = client.darkstorage.post("/v1/buckets", json=new_bucket)
print(f"Created bucket: {response.json()}")

# Upload a file (assuming multipart/form-data or presigned URL)
upload_request = {
    "bucket": "my-app-data",
    "key": "documents/report.pdf",
    "content_type": "application/pdf"
}
response = client.darkstorage.post("/v1/upload", json=upload_request)
upload_url = response.json()["upload_url"]
print(f"Upload URL: {upload_url}")

# List files in a bucket
response = client.darkstorage.get("/v1/buckets/my-app-data/objects")
files = response.json()
print(f"Files in bucket: {files}")

# Get file metadata
response = client.darkstorage.get("/v1/buckets/my-app-data/objects/documents/report.pdf")
metadata = response.json()
print(f"File metadata: {metadata}")

# Generate a presigned download URL
response = client.darkstorage.post(
    "/v1/buckets/my-app-data/objects/documents/report.pdf/presign",
    json={"expires_in": 3600}
)
download_url = response.json()["download_url"]
print(f"Download URL: {download_url}")

# Delete a file
response = client.darkstorage.delete("/v1/buckets/my-app-data/objects/documents/report.pdf")
print(f"File deleted: {response.status_code == 204}")

# Delete a bucket
response = client.darkstorage.delete("/v1/buckets/my-app-data")
print(f"Bucket deleted: {response.status_code == 204}")

client.close_all()
