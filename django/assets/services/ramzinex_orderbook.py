# assets/services/ramzinex_orderbook.py
from assets.models import Asset  # Changed from CustomAsset
from assets.exchanges.ramzinex import RamzinexAPI
import asyncio

def update_orderbook(data):
    """
    Callback function to handle incoming order book data.
    """
    sells = data.get('sells', [])
    buys = data.get('buys', [])
    last_trade_price = data.get('lastTradePrice')
    last_update = data.get('lastUpdate')

    # Update or create CustomAsset records based on the order book data
    for sell in sells:
        price, quantity = float(sell[0]), float(sell[1])
        CustomAsset.objects.update_or_create(
            name='Sell Order',
            defaults={
                'quantity': quantity,
                'initial_price': price,
                'asset_type': 'crypto',
                'exchange_name': 'Ramzinex',
            }
        )

    for buy in buys:
        price, quantity = float(buy[0]), float(buy[1])
        CustomAsset.objects.update_or_create(
            name='Buy Order',
            defaults={
                'quantity': quantity,
                'initial_price': price,
                'asset_type': 'crypto',
                'exchange_name': 'Ramzinex',
            }
        )

async def import_ramzinex_orderbook(pair_id):
    """
    Imports order book data from Ramzinex WebSocket API.
    """
    ramzinex_api = RamzinexAPI()
    await ramzinex_api.connect()
    ramzinex_api.subscribe_to_orderbook(pair_id, update_orderbook)
    await ramzinex_api.run()