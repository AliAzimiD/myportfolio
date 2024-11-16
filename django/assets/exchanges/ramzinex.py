# assets/exchanges/ramzinex.py
import requests
from django.conf import settings
from .base import ExchangeAPI
import asyncio
from centrifuge import Client as CentrifugeClient

class RamzinexAPI(ExchangeAPI):
    """Class for interacting with the Ramzinex exchange API and WebSocket."""

    def __init__(self):
        super().__init__(
            base_url="https://ramzinex.com/exchange/api/v1.0/",
            api_key=settings.RAMZINEX_API_KEY,
            api_token=settings.RAMZINEX_API_TOKEN
        )
        self.ws_url = 'wss://websocket.ramzinex.com/websocket'
        self.client = CentrifugeClient(self.ws_url)
        self.channels = []

    async def connect(self):
        await self.client.connect()
        print("Connected to Ramzinex WebSocket")

    def subscribe_to_orderbook(self, pair_id, callback):
        channel = f'orderbook:{pair_id}'
        self.channels.append(channel)
        sub = self.client.new_subscription(channel)

        @sub.on('publication')
        def on_publication(ctx):
            data = ctx['data']
            callback(data)

        sub.subscribe()

    async def run(self):
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            await self.client.close()

    def fetch_currencies(self):
        """
        Fetches a mapping of currency IDs to their symbols from Ramzinex.
        This is necessary because balance data uses currency IDs.
        """
        url = "https://ramzinex.com/exchange/api/v2.0/exchange/currencies"
        try:
            response = requests.get(url)  # No headers needed for public API
            response.raise_for_status()
            currencies_response = response.json()
            if currencies_response and 'data' in currencies_response and 'currencies' in currencies_response['data']:
                currencies_list = currencies_response['data']['currencies']
                # Create a dictionary mapping currency_id to symbol (e.g., {1: 'BTC'})
                currency_map = {currency['id']: currency['symbol'].upper() for currency in currencies_list}
                return currency_map
            else:
                print("Error: Unexpected response format from Ramzinex API for currencies.")
                return None
        except requests.RequestException as err:
            print(f"Request error: {err}")
            return None


    def fetch_balances(self):
        """
        Fetches the user's account balances from Ramzinex and adds currency symbols to the data.
        """
        currency_map = self.fetch_currencies()
        if not currency_map:
            print("Error: Could not fetch currency mapping.")
            return None

        endpoint = "users/me/funds/summaryDesktop"
        balances_response = self.get(endpoint)
        if balances_response and 'data' in balances_response:
            balances = balances_response['data']
            # Add 'currency_symbol' to each balance using the currency_map
            for balance in balances:
                currency_id = balance.get('currency_id')
                balance['currency_symbol'] = currency_map.get(currency_id, 'UNKNOWN')
            return balances
        else:
            print("Error: Unexpected response format from Ramzinex API for balances.")
            return None

    # Implement fetch_transactions if needed
    def fetch_transactions(self):
        """
        Fetches the user's transaction history from Ramzinex.
        """
        endpoint = "users/me/orders3"
        data = {
            "offset": 0,
            "limit": 100  # Adjust as needed
        }
        transactions_response = self.post(endpoint, data=data)
        if transactions_response and 'data' in transactions_response:
            return transactions_response['data']
        else:
            print("Error: Unexpected response format from Ramzinex API for transactions.")
            return None