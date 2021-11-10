# Generated by Django 3.2.9 on 2021-11-10 16:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('title', models.TextField(max_length=200)),
                ('startingBalance', models.DecimalField(decimal_places=2, max_digits=14)),
                ('rules', models.TextField(max_length=200)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('winner', models.CharField(blank=True, max_length=200, null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Portfolio',
            fields=[
                ('title', models.TextField(max_length=200)),
                ('cash_balance', models.DecimalField(decimal_places=2, default=10000.0, max_digits=14)),
                ('equity_value', models.DecimalField(decimal_places=2, default=0.0, max_digits=14)),
                ('total_value', models.DecimalField(decimal_places=2, default=10000.0, max_digits=14)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('game', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='trade_simulation.game')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('ticker', models.TextField(max_length=200)),
                ('tradeType', models.TextField(max_length=200)),
                ('shares', models.IntegerField()),
                ('bought_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=14)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('portfolio', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='trade_simulation.portfolio')),
            ],
        ),
        migrations.CreateModel(
            name='Holding',
            fields=[
                ('ticker', models.TextField(max_length=200)),
                ('shares', models.IntegerField()),
                ('current_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=14)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('portfolio', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='trade_simulation.portfolio')),
            ],
        ),
    ]
