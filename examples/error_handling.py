"""Example with error handling."""
from aftershipstorage import AftershipStorage
import requests

client = AftershipStorage.from_env()

try:
    # Make API call that might fail
    response = client.darkship.get("/v1/shipments/nonexistent-id")
    print("Success:", response.json())

except requests.HTTPError as e:
    # Handle HTTP errors (4xx, 5xx)
    print(f"HTTP Error: {e.response.status_code}")
    print(f"Response: {e.response.text}")

except requests.ConnectionError:
    # Handle connection errors
    print("Failed to connect to the API")

except requests.Timeout:
    # Handle timeout errors
    print("Request timed out")

except ValueError as e:
    # Handle cases where client wasn't initialized
    print(f"Client error: {e}")

except Exception as e:
    # Handle any other errors
    print(f"Unexpected error: {e}")

finally:
    client.close_all()
