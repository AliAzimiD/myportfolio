# assets/exchanges/base.py
import requests
from django.conf import settings

# assets/exchanges/base.py
import requests

class ExchangeAPI:
    """Base class for cryptocurrency exchange APIs."""

    def __init__(self, base_url, api_key, api_token):
        if not api_key or not api_token:
            raise ValueError("API key and token must be provided.")
        self.base_url = base_url
        self.api_key = api_key
        self.api_token = api_token

    def get_headers(self):
        """
        Generate headers required for API requests.
        """
        return {
            "Authorization2": f"Bearer {self.api_token}",
            "x-api-key": self.api_key,
            "Accept": "application/json"
        }

    def get(self, endpoint, params=None):
        """GET request to the exchange API."""
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.get(url, headers=self.get_headers(), params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err} - Status code: {response.status_code}")
            print(f"Response content: {response.content.decode()}")
            return None
        except requests.exceptions.RequestException as req_err:
            print(f"Request error occurred: {req_err}")
            return None

    def post(self, endpoint, data=None):
        """POST request to the exchange API."""
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.post(url, headers=self.get_headers(), json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err} - Status code: {response.status_code}")
            print(f"Response content: {response.content.decode()}")
            return None
        except requests.exceptions.RequestException as req_err:
            print(f"Request error occurred: {req_err}")
            return None

    # Define other methods as needed
    def fetch_balances(self):
        raise NotImplementedError("Subclasses must implement fetch_balances method")

    def fetch_transactions(self):
        raise NotImplementedError("Subclasses must implement fetch_transactions method")
