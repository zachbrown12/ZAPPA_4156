from django.db import models
from django.contrib.auth.models import User
import uuid
from yfinance import Ticker


class Game(models.Model):
    title = models.TextField(max_length=200, unique=True)
    starting_balance = models.DecimalField(
        max_digits=14, decimal_places=2, default=10000.00
    )
    rules = models.TextField(max_length=200)
    winner = models.CharField(max_length=200, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    uid = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    def __str__(self):
        return self.title

    def rank_portfolios(self):
        portfolios = Portfolio.objects.filter(game=self)
        for portfolio in portfolios:
            portfolio.compute_total_value()
        leaderboard = sorted(portfolios, key=lambda p: p.total_value, reverse=True)
        print(leaderboard)
        for i in range(len(leaderboard)):
            if (i > 0) and (
                leaderboard[i].total_value == leaderboard[i - 1].total_value
            ):
                leaderboard[i].game_rank = leaderboard[i - 1].game_rank
            else:
                leaderboard[i].game_rank = i + 1
            leaderboard[i].save()


class Portfolio(models.Model):
    owner = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, null=True, blank=True, on_delete=models.CASCADE)
    game_rank = models.IntegerField(null=True, blank=True)
    title = models.TextField(max_length=200)
    cash_balance = models.DecimalField(max_digits=14, decimal_places=2, default=10000.00)
    total_value = models.DecimalField(max_digits=14, decimal_places=2, default=10000.00)
    created_on = models.DateTimeField(auto_now_add=True)
    uid = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    class Meta:
        unique_together = ('title', 'game',)

    def __str__(self):
        return self.title

    def equity_value(self):
        value = 0
        holdings = Holding.objects.filter(portfolio=self)
        for holding in holdings:
            value += (holding.shares * holding.current_price)

        if len(holdings) > 0:
            return value
        else:
            return 0

    def total_value(self):
        total = self.equity_value() + self.cash_balance
        return total 


class Holding(models.Model):
    portfolio =  models.ForeignKey(
        Portfolio, null=True, blank=True, on_delete=models.CASCADE)
    ticker = models.TextField(max_length=200)
    shares = models.DecimalField(max_digits=14, decimal_places=2, default=0.00, null=True)
    current_price = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)
    created_on = models.DateTimeField(auto_now_add=True)
    uid = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    def __str__(self):
        return self.ticker

    @property
    def getValue(self):
        value = self.current_price * self.shares
        self.value = value
        self.save()

class Transaction(models.Model):
    portfolio =  models.ForeignKey(
        Portfolio, null=True, blank=True, on_delete=models.CASCADE)
    ticker = models.TextField(max_length=200)
    tradeType = models.TextField(max_length=200)
    shares = models.DecimalField(max_digits=14, decimal_places=2, default=0.00, null=True)
    bought_price = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)
    created_on = models.DateTimeField(auto_now_add=True)
    uid = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    def __str__(self):
        return (self.ticker)

    
