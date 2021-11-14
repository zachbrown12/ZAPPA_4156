from django.db import models
from django.contrib.auth.models import User
import uuid
from yfinance import Ticker


class Game(models.Model):
    title = models.TextField(max_length=200)
    startingBalance = models.DecimalField(
        max_digits=14, decimal_places=2, default=10000.00
    )
    rules = models.TextField(max_length=200)
    winner = models.CharField(max_length=200, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    def rank_portfolios(self):
        portfolios = Portfolio.objects.filter(game=self)
        for portfolio in portfolios:
            portfolio.computeTotalValue()
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
    cash_balance = models.DecimalField(
        max_digits=14, decimal_places=2, default=10000.00
    )
    total_value = models.DecimalField(max_digits=14, decimal_places=2, default=10000.00)
    created_on = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    def __str__(self):
        return self.title

    def equity_value(self):
        value = 0
        holdings = Holding.objects.filter(portfolio=self)
        if not holdings:
            return 0
        for holding in holdings:
            value += holding.market_value()
        return value

    def compute_total_value(self):
        self.total_value = self.equity_value() + float(self.cash_balance)
        self.save()

    # Create a transaction record
    def add_transaction(self, ticker, shares, price, type):
        transaction = Transaction.objects.create()
        transaction.portfolio = self
        transaction.ticker = ticker
        transaction.tradeType = type
        transaction.shares = shares
        transaction.bought_price = price
        transaction.save()

    # Buy <shares> shares of stock <ticker>
    def buy_holding(self, ticker, shares):
        holding, created = Holding.objects.get_or_create(portfolio=self, ticker=ticker)

        price = holding.askprice()
        if price is None:
            print("Ticker {} is not currently traded.".format(ticker))
            return
        cost = price * float(shares)
        if float(self.cash_balance) < cost:
            print("Not enough cash to buy ${} of {}.".format(cost, ticker))
            return
        holding.shares = float(0 if holding.shares is None else holding.shares) + float(
            shares
        )
        holding.save()

        self.cash_balance = float(self.cash_balance) - cost
        self.save()

        self.addTransaction(ticker, shares, price, "Buy")

    # Sell <shares> shares of stock <ticker>
    def sell_holding(self, ticker, shares):
        holding = Holding.objects.get(portfolio=self, ticker=ticker)
        if not holding:
            print("Holding {} is not in portfolio.".format(ticker))
            return
        price = holding.bidprice()
        if price is None:
            print("Ticker {} is not currently traded.".format(ticker))
            return
        currentshares = float(0 if holding.shares is None else holding.shares)
        if currentshares < float(shares):
            print("Not enough shares of {} to sell {}.".format(ticker, float(shares)))
            return
        holding.shares = currentshares - float(shares)
        if holding.shares == 0.0:
            holding.delete()
        else:
            holding.save()

        self.cash_balance = float(self.cash_balance) + (price * float(shares))
        self.save()

        self.addTransaction(ticker, shares, price, "Sell")


class Holding(models.Model):
    portfolio = models.ForeignKey(
        Portfolio, null=True, blank=True, on_delete=models.CASCADE
    )
    ticker = models.TextField(max_length=200)
    shares = models.DecimalField(
        max_digits=14, decimal_places=2, default=0.00, null=True
    )
    created_on = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    def __str__(self):
        return self.ticker

    # Get the ask price (what you can buy immediately for)
    def ask_price(self):
        stockInfo = Ticker(str(self.ticker)).info
        if "ask" not in stockInfo:
            return None
        if stockInfo["ask"] == 0:
            return stockInfo["regularMarketPrice"]
        return stockInfo["ask"]

    # Get the bid price (what you can sell immediately for)
    def bid_price(self):
        stockInfo = Ticker(str(self.ticker)).info
        if "bid" not in stockInfo:
            return None
        if stockInfo["bid"] == 0:
            return stockInfo["regularMarketPrice"]
        return stockInfo["bid"]

    def market_value(self):
        return self.bidprice() * float(self.shares)


class Transaction(models.Model):
    portfolio = models.ForeignKey(
        Portfolio, null=True, blank=True, on_delete=models.CASCADE
    )
    ticker = models.TextField(max_length=200)
    tradeType = models.TextField(max_length=200)
    shares = models.DecimalField(
        max_digits=14, decimal_places=2, default=0.00, null=True
    )
    bought_price = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)
    created_on = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    def __str__(self):
        return self.ticker
