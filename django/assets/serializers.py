# assets/serializers.py
from rest_framework import serializers
from .models import Asset, Transaction  # Changed from CustomAsset

class CustomAssetSerializer(serializers.ModelSerializer):
    # Serializer for converting CustomAsset instances to and from JSON
    class Meta:
        model = Asset  # Changed from CustomAsset
        fields = ['id', 'name', 'asset_type', 'quantity', 'value_usd', 'value_toman', 
                 'purchase_value_usd', 'exchange_name', 'purchase_date', 'user']
        read_only_fields = ['user']

class TransactionSerializer(serializers.ModelSerializer):
    # Serializer for Transaction instances
    class Meta:
        model = Transaction
        fields = ['id', 'asset', 'transaction_type', 'amount', 'transaction_date', 'price_at_transaction', 'transaction_id']
