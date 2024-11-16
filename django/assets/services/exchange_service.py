# assets/services/exchange_service.py
from typing import Optional, List
import logging
from datetime import datetime
from decimal import Decimal

from assets.models import CustomAsset, Transaction
from assets.exchanges.ramzinex import RamzinexAPI
from .handlers import BalanceHandler, TransactionHandler

logger = logging.getLogger(__name__)

def import_ramzinex_balances() -> Optional[List[CustomAsset]]:
    """Service function to import balances from Ramzinex."""
    service = RamzinexService()
    return service.import_balances()

def import_ramzinex_transactions() -> Optional[List[Transaction]]:
    """Service function to import transactions from Ramzinex."""
    service = RamzinexService()
    return service.import_transactions()

class RamzinexService:
    """Service layer for handling Ramzinex exchange operations."""
    
    def __init__(self):
        self.api = RamzinexAPI()
        self.balance_handler = BalanceHandler()
        self.transaction_handler = TransactionHandler()

    # ...existing methods...
    def import_balances(self) -> Optional[List[CustomAsset]]:
        """
        Import and process balances from Ramzinex API.
        
        Returns:
            List[CustomAsset]: List of imported/updated assets or None if failed
        """
        try:
            balances_data = self.api.fetch_balances()
            if not balances_data:
                logger.warning("No balances data received from Ramzinex API")
                return None
                
            return self.balance_handler.process_balances(balances_data)
            
        except Exception as e:
            logger.error(f"Failed to import balances: {str(e)}")
            return None

    def import_transactions(self) -> Optional[List[Transaction]]:
        """
        Import and process transactions from Ramzinex API.
        
        Returns:
            List[Transaction]: List of imported/updated transactions or None if failed
        """
        try:
            transactions_data = self.api.fetch_transactions()
            if not transactions_data:
                logger.warning("No transactions data received from Ramzinex API")
                return None
                
            return self.transaction_handler.process_transactions(transactions_data)
            
        except Exception as e:
            logger.error(f"Failed to import transactions: {str(e)}")
            return None
