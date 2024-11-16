# assets/services/handlers.py
from typing import Dict, List, Any, Optional
from datetime import datetime
from decimal import Decimal

from assets.models import CustomAsset, Transaction

class BalanceHandler:
    """Handles processing of balance data from Ramzinex API."""
    
    def process_balances(self, balances_data: List[Dict[str, Any]]) -> List[CustomAsset]:
        imported_assets = []
        
        for balance in balances_data:
            asset = self._process_single_balance(balance)
            if asset:
                imported_assets.append(asset)
                
        return imported_assets
    
    def _process_single_balance(self, balance: Dict[str, Any]) -> Optional[CustomAsset]:
        currency_symbol = balance.get('currency_symbol')
        total_balance = Decimal(str(balance.get('total_nr', 0)))
        
        asset, created = CustomAsset.objects.get_or_create(
            name=currency_symbol,
            asset_type='crypto',
            exchange_name="Ramzinex",
            defaults={
                'quantity': total_balance,
                'initial_price': Decimal('0'),
                'purchase_date': None,
                'wallet_id': None
            }
        )
        
        if not created:
            asset.quantity = total_balance
            asset.save()
            
        return asset

class TransactionHandler:
    """Handles processing of transaction data from Ramzinex API."""
    
    # ...existing methods...