# django/assets/tasks.py
from apscheduler.schedulers.background import BackgroundScheduler
# from .models import CryptoAsset
# from .utils import fetch_crypto_price
from decimal import Decimal


# def update_crypto_prices():
#     """Fetch and update prices for all crypto assets in the portfolio."""
#     assets = CryptoAsset.objects.all()
#     for asset in assets:
#         price = fetch_crypto_price(asset.symbol)
#         if price is not None:
#             asset.current_value = Decimal(price) * asset.quantity  # Convert price to Decimal
#             asset.save()
#             print(f"Updated {asset.name} to ${asset.current_value}")
#         else:
#             print(f"Failed to update {asset.name}")

# def start_scheduler():
#     scheduler = BackgroundScheduler()
#     scheduler.add_job(update_crypto_prices, 'interval', minutes=10)  # Update every 10 minutes
#     scheduler.start()
