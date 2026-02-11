"""Base HTTP client for making authenticated requests."""
import requests
from typing import Optional, Dict, Any, Union
from urllib.parse import urljoin


class BaseClient:
    """Base HTTP client with API key authentication."""

    def __init__(self, base_url: str, api_key: str, api_key_header: str = "X-API-Key"):
        """
        Initialize the base client.

        Args:
            base_url: Base URL for the API (e.g., "https://api.darkship.io")
            api_key: API key for authentication
            api_key_header: Header name for the API key (default: "X-API-Key")
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.api_key_header = api_key_header
        self.session = requests.Session()
        self.session.headers.update({
            self.api_key_header: self.api_key,
            "Content-Type": "application/json",
            "User-Agent": "aftershipstorage-python-client/0.1.0"
        })

    def _build_url(self, endpoint: str) -> str:
        """Build full URL from endpoint."""
        endpoint = endpoint.lstrip('/')
        return urljoin(f"{self.base_url}/", endpoint)

    def request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs
    ) -> requests.Response:
        """
        Make an HTTP request.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE, etc.)
            endpoint: API endpoint path
            params: Query parameters
            data: Form data
            json: JSON body
            headers: Additional headers
            **kwargs: Additional arguments to pass to requests

        Returns:
            Response object

        Raises:
            requests.HTTPError: If the request fails
        """
        url = self._build_url(endpoint)

        request_headers = {}
        if headers:
            request_headers.update(headers)

        response = self.session.request(
            method=method,
            url=url,
            params=params,
            data=data,
            json=json,
            headers=request_headers,
            **kwargs
        )

        response.raise_for_status()
        return response

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None, **kwargs) -> requests.Response:
        """Make a GET request."""
        return self.request("GET", endpoint, params=params, **kwargs)

    def post(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> requests.Response:
        """Make a POST request."""
        return self.request("POST", endpoint, data=data, json=json, **kwargs)

    def put(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> requests.Response:
        """Make a PUT request."""
        return self.request("PUT", endpoint, data=data, json=json, **kwargs)

    def patch(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> requests.Response:
        """Make a PATCH request."""
        return self.request("PATCH", endpoint, data=data, json=json, **kwargs)

    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        """Make a DELETE request."""
        return self.request("DELETE", endpoint, **kwargs)

    def close(self):
        """Close the session."""
        self.session.close()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
