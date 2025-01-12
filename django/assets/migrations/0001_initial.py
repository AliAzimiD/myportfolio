# Generated by Django 3.2.25 on 2024-11-16 21:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('asset_type', models.CharField(choices=[('crypto', 'Cryptocurrency'), ('stock', 'Stock'), ('forex', 'Forex'), ('commodity', 'Commodity'), ('other', 'Other')], max_length=50)),
                ('quantity', models.DecimalField(decimal_places=8, max_digits=18)),
                ('initial_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('purchase_date', models.DateField()),
                ('exchange_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_type', models.CharField(max_length=50)),
                ('amount', models.DecimalField(decimal_places=8, max_digits=18)),
                ('transaction_date', models.DateTimeField(auto_now_add=True)),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assets.asset')),
            ],
        ),
        migrations.CreateModel(
            name='CustomAssetType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='asset',
            name='custom_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='assets.customassettype'),
        ),
        migrations.AddField(
            model_name='asset',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
