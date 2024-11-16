# django/assets/utils.py
import requests

def get_coingecko_ids():
    # Known mappings for major assets
    symbol_to_id = {
        'BTC': 'bitcoin',
        'ETH': 'ethereum',
        # Add additional well-known mappings if needed
    }

    # Fetch all available IDs from CoinGecko and add to dictionary for other assets
    try:
        response = requests.get("https://api.coingecko.com/api/v3/coins/list")
        response.raise_for_status()
        coins = response.json()
        for coin in coins:
            symbol = coin['symbol'].upper()
            if symbol not in symbol_to_id:  # Avoid overwriting known symbols
                symbol_to_id[symbol] = coin['id']
        return symbol_to_id
    except requests.RequestException as e:
        print(f"Error fetching CoinGecko IDs: {e}")
        return {}

COINGECKO_API_URL = "https://api.coingecko.com/api/v3/simple/price"

# Fetch the symbol-to-ID mapping once
SYMBOL_TO_ID = get_coingecko_ids()

def fetch_crypto_price(symbol):
    """Fetch the current price for a cryptocurrency using its symbol."""
    coin_id = SYMBOL_TO_ID.get(symbol.upper())
    if not coin_id:
        print(f"CoinGecko ID not found for symbol: {symbol}")
        return None
    try:
        response = requests.get(
            COINGECKO_API_URL,
            params={
                'ids': coin_id,
                'vs_currencies': 'usd'
            }
        )
        response.raise_for_status()
        data = response.json()
        return data[coin_id]['usd']
    except (requests.RequestException, KeyError) as e:
        print(f"Error fetching price for {symbol}: {e}")
        return None