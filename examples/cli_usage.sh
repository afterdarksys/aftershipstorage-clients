#!/bin/bash
# Example: Using the aftership CLI

# Initialize configuration
echo "Creating config file..."
aftership config init --minimal

echo ""
echo "Edit aftership.yaml and add your API keys, then run:"
echo ""

# Example commands (commented out - add your API keys first)
echo "# Darkship - List shipments"
echo "aftership darkship get /v1/shipments --format table"
echo ""

echo "# Darkstorage - List buckets"
echo "aftership darkstorage get /v1/buckets"
echo ""

echo "# Shipshack - List ships"
echo "aftership shipshack get /v1/ships --format table"
echo ""

echo "# Models2go - List models"
echo "aftership models2go get /v1/models"
echo ""

echo "# Hostscience - List instances"
echo "aftership hostscience get /v1/instances --format yaml"
echo ""

echo "# Aiserve - List compute jobs"
echo "aftership aiserve get /v1/compute/jobs"
echo ""

echo "# Create a new shipment"
echo "aftership darkship post /v1/shipments --data '{\"tracking_number\": \"TEST123\", \"carrier\": \"FedEx\"}'"
echo ""

echo "# Create a storage bucket"
echo "aftership darkstorage post /v1/buckets --data '{\"name\": \"my-bucket\", \"region\": \"us-west-1\"}'"
echo ""

echo "# Create an AI training job"
echo "aftership aiserve post /v1/compute/jobs --data '{\"name\": \"train-model\", \"gpu_type\": \"A100\"}'"
echo ""

echo "# Show current config"
echo "aftership config show"
