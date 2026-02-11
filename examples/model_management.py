"""Example: Publishing and managing models on models2go.com."""
from aftershipstorage import AftershipStorage

client = AftershipStorage.from_env()

# List all published models
response = client.models2go.get("/v1/models")
models = response.json()
print(f"Published models: {models}")

# Publish a new model
new_model = {
    "name": "text-classifier-v1",
    "description": "A fine-tuned text classification model",
    "version": "1.0.0",
    "framework": "pytorch",
    "file_url": "https://storage.example.com/models/classifier.pt",
    "metadata": {
        "accuracy": 0.95,
        "training_date": "2026-02-01",
        "dataset": "custom-dataset-v1"
    },
    "tags": ["nlp", "classification", "production"]
}
response = client.models2go.post("/v1/models", json=new_model)
model = response.json()
print(f"Published model: {model}")

# Get model details
model_id = model["id"]
response = client.models2go.get(f"/v1/models/{model_id}")
details = response.json()
print(f"Model details: {details}")

# Update model metadata
updates = {
    "description": "Updated: A fine-tuned text classification model with improved accuracy",
    "metadata": {
        "accuracy": 0.97,
        "last_updated": "2026-02-11"
    }
}
response = client.models2go.patch(f"/v1/models/{model_id}", json=updates)
updated_model = response.json()
print(f"Updated model: {updated_model}")

# List model versions
response = client.models2go.get(f"/v1/models/{model_id}/versions")
versions = response.json()
print(f"Model versions: {versions}")

# Publish a new version
new_version = {
    "version": "1.1.0",
    "file_url": "https://storage.example.com/models/classifier-v1.1.pt",
    "changelog": "Improved accuracy on edge cases"
}
response = client.models2go.post(f"/v1/models/{model_id}/versions", json=new_version)
version = response.json()
print(f"Published version: {version}")

# Download model (get download URL)
response = client.models2go.get(f"/v1/models/{model_id}/download")
download_info = response.json()
print(f"Download URL: {download_info['download_url']}")

# Get model usage statistics
response = client.models2go.get(f"/v1/models/{model_id}/stats")
stats = response.json()
print(f"Model stats: {stats}")

# Unpublish/delete a model
response = client.models2go.delete(f"/v1/models/{model_id}")
print(f"Model deleted: {response.status_code == 204}")

client.close_all()
