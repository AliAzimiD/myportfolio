# assets/models.py
from django.db import models
from django.contrib.auth.models import User

class CustomAssetType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Asset(models.Model):
    ASSET_TYPES = [
        ('crypto', 'Cryptocurrency'),
        ('stock', 'Stock'),
        ('forex', 'Forex'),
        ('commodity', 'Commodity'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=100)
    asset_type = models.CharField(
        max_length=50,
        choices=ASSET_TYPES,
    )
    custom_type = models.ForeignKey(
        CustomAssetType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    quantity = models.DecimalField(max_digits=18, decimal_places=8)
    initial_price = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_date = models.DateField()
    exchange_name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_asset_type_display(self):
        if self.custom_type:
            return self.custom_type.name
        return dict(self.ASSET_TYPES).get(self.asset_type, '')

    def __str__(self):
        return f"{self.name} ({self.get_asset_type_display()})"

class Transaction(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)  # Updated reference
    transaction_type = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=18, decimal_places=8)
    transaction_date = models.DateTimeField(auto_now_add=True)