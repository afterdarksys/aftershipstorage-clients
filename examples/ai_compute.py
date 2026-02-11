"""Example: AI compute management via aiserve.farm."""
from aftershipstorage import AftershipStorage

client = AftershipStorage.from_env()

# List available AI compute resources
response = client.aiserve.get("/v1/compute/resources")
resources = response.json()
print(f"Available AI compute resources: {resources}")

# Create a new AI compute job
job = {
    "name": "train-sentiment-model",
    "type": "training",
    "framework": "pytorch",
    "gpu_type": "A100",
    "gpu_count": 4,
    "cpu_cores": 32,
    "memory": 128,
    "memory_unit": "GB",
    "storage": 500,
    "storage_unit": "GB",
    "docker_image": "pytorch/pytorch:2.0.0-cuda11.8-cudnn8-runtime",
    "command": "python train.py --epochs 100 --batch-size 64",
    "environment": {
        "WANDB_API_KEY": "your-wandb-key",
        "DATA_PATH": "/data/training"
    }
}
response = client.aiserve.post("/v1/compute/jobs", json=job)
created_job = response.json()
print(f"Created job: {created_job}")

# Get job details
job_id = created_job["id"]
response = client.aiserve.get(f"/v1/compute/jobs/{job_id}")
job_details = response.json()
print(f"Job details: {job_details}")

# List all jobs
response = client.aiserve.get("/v1/compute/jobs")
all_jobs = response.json()
print(f"All jobs: {all_jobs}")

# Get job status and metrics
response = client.aiserve.get(f"/v1/compute/jobs/{job_id}/status")
status = response.json()
print(f"Job status: {status}")

response = client.aiserve.get(f"/v1/compute/jobs/{job_id}/metrics")
metrics = response.json()
print(f"Job metrics: {metrics}")

# Get job logs
response = client.aiserve.get(
    f"/v1/compute/jobs/{job_id}/logs",
    params={"lines": 100, "follow": False}
)
logs = response.json()
print(f"Recent logs:\n{logs['logs']}")

# Create an inference endpoint
inference_endpoint = {
    "name": "sentiment-analyzer-api",
    "model_path": "https://darkstorage.io/models/sentiment-v2.pt",
    "framework": "pytorch",
    "gpu_type": "T4",
    "gpu_count": 1,
    "cpu_cores": 4,
    "memory": 16,
    "memory_unit": "GB",
    "docker_image": "pytorch/pytorch:2.0.0-cuda11.8-cudnn8-runtime",
    "scaling": {
        "min_replicas": 1,
        "max_replicas": 10,
        "target_cpu_utilization": 70
    },
    "health_check": {
        "path": "/health",
        "interval": 30,
        "timeout": 5
    }
}
response = client.aiserve.post("/v1/inference/endpoints", json=inference_endpoint)
endpoint = response.json()
print(f"Created inference endpoint: {endpoint}")

# Get endpoint details
endpoint_id = endpoint["id"]
response = client.aiserve.get(f"/v1/inference/endpoints/{endpoint_id}")
endpoint_details = response.json()
print(f"Endpoint URL: {endpoint_details['url']}")
print(f"Endpoint status: {endpoint_details['status']}")

# Scale endpoint
scale_config = {
    "min_replicas": 2,
    "max_replicas": 20
}
response = client.aiserve.patch(
    f"/v1/inference/endpoints/{endpoint_id}/scale",
    json=scale_config
)
scaled_endpoint = response.json()
print(f"Scaled endpoint: {scaled_endpoint}")

# Get endpoint metrics
response = client.aiserve.get(
    f"/v1/inference/endpoints/{endpoint_id}/metrics",
    params={"period": "1h"}
)
endpoint_metrics = response.json()
print(f"Endpoint metrics: {endpoint_metrics}")

# Create a batch inference job
batch_job = {
    "name": "batch-sentiment-analysis",
    "model_endpoint_id": endpoint_id,
    "input_data_url": "https://darkstorage.io/data/batch-input.jsonl",
    "output_data_url": "https://darkstorage.io/data/batch-output.jsonl",
    "batch_size": 32,
    "max_concurrent_requests": 10
}
response = client.aiserve.post("/v1/inference/batch", json=batch_job)
batch_job_info = response.json()
print(f"Created batch job: {batch_job_info}")

# Monitor batch job
batch_job_id = batch_job_info["id"]
response = client.aiserve.get(f"/v1/inference/batch/{batch_job_id}")
batch_status = response.json()
print(f"Batch job progress: {batch_status['progress']}%")

# Reserve GPU resources for future use
reservation = {
    "name": "research-cluster",
    "gpu_type": "A100",
    "gpu_count": 8,
    "start_time": "2026-02-15T00:00:00Z",
    "duration_hours": 168,
    "priority": "high"
}
response = client.aiserve.post("/v1/compute/reservations", json=reservation)
reservation_info = response.json()
print(f"Created reservation: {reservation_info}")

# List GPU availability
response = client.aiserve.get(
    "/v1/compute/availability",
    params={"gpu_type": "A100", "region": "us-west-1"}
)
availability = response.json()
print(f"GPU availability: {availability}")

# Get pricing information
response = client.aiserve.get("/v1/pricing")
pricing = response.json()
print(f"Pricing: {pricing}")

# Stop a training job
response = client.aiserve.post(f"/v1/compute/jobs/{job_id}/stop")
print(f"Job stopped: {response.json()}")

# Delete an inference endpoint
response = client.aiserve.delete(f"/v1/inference/endpoints/{endpoint_id}")
print(f"Endpoint deleted: {response.status_code == 204}")

# Cancel a reservation
response = client.aiserve.delete(f"/v1/compute/reservations/{reservation_info['id']}")
print(f"Reservation cancelled: {response.status_code == 204}")

client.close_all()
