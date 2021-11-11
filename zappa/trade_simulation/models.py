from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.


class Game(models.Model):
    title = models.TextField(max_length=200)
    startingBalance = models.DecimalField(max_digits=14, decimal_places=2)
    rules = models.TextField(max_length=200)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    winner = models.CharField(max_length=200, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )


class Portfolio(models.Model):
    owner = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, null=True, blank=True, on_delete=models.CASCADE)
    title = models.TextField(max_length=200)
    cash_balance = models.DecimalField(max_digits=14, decimal_places=2)
    equity_value = models.DecimalField(max_digits=14, decimal_places=2)
    total_value = models.DecimalField(max_digits=14, decimal_places=2)
    created_on = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    def __str__(self):
        return self.title


class Stock(models.Model):
    ticker = models.TextField(max_length=200)
    current_price = models.DecimalField(max_digits=14, decimal_places=2)
    created_on = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    def __str__(self):
        return self.ticker


class Transaction(models.Model):
    portfolio = models.ForeignKey(
        Portfolio, null=True, blank=True, on_delete=models.CASCADE
    )
    stock = models.ForeignKey(Stock, null=True, blank=True, on_delete=models.CASCADE)
    tradeType = models.TextField(max_length=200)
    shares = models.IntegerField()
    created_on = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    def __str__(self):
        return self.title
