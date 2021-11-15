from django.db import models
from django.contrib.auth.models import User
import uuid
from yfinance import Ticker

TRANSACTION_TYPE_BUY = "BUY"
TRANSACTION_TYPE_SELL = "SELL"


class Game(models.Model):
    """
    Game represents environment where users can create their portfolios
    and compete for the highest valued portfolio
    """

    # Title is a unique identifier for the game
    title = models.TextField(max_length=200, unique=True)
    starting_balance = models.DecimalField(
        max_digits=14, decimal_places=2, default=10000.00
    )
    rules = models.TextField(max_length=200)
    # Winner is set once a user has won the game at the conclusion of the game
    winner = models.CharField(max_length=200, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    uid = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    def __str__(self):
        """
        Return string representation of game
        """
        return self.title

    def rank_portfolios(self):
        """
        rank_portfolios iterates through all portfolios in the game to
        compute their total value and ranks the portfolios based on this value
        Returns: list of portfolios ordered by ranking
        """
        portfolios = Portfolio.objects.filter(game=self)
        for portfolio in portfolios:
            portfolio.compute_total_value()

        leaderboard = sorted(portfolios, key=lambda p: p.total_value, reverse=True)
        for i in range(len(leaderboard)):
            if (i > 0) and (
                leaderboard[i].total_value == leaderboard[i - 1].total_value
            ):
                leaderboard[i].game_rank = leaderboard[i - 1].game_rank
            else:
                leaderboard[i].game_rank = i + 1
            leaderboard[i].save()
        return leaderboard


class Portfolio(models.Model):
    """
    Portfolio is the representation of a user's stock portfolio
    """

    owner = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    # Each portfolio is associated with a game in progress
    game = models.ForeignKey(Game, null=True, blank=True, on_delete=models.CASCADE)
    # All portfolios are tied for first place to begin
    game_rank = models.IntegerField(default=1)
    title = models.TextField(max_length=200)
    cash_balance = models.DecimalField(
        max_digits=14, decimal_places=2, default=10000.00
    )
    total_value = models.DecimalField(max_digits=14, decimal_places=2, default=10000.00)
    created_on = models.DateTimeField(auto_now_add=True)
    uid = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    class Meta:
        unique_together = ("title", "game")

    def __str__(self):
        """
        String representation of a portfolio
        """
        return self.title

    def equity_value(self):
        """
        equity_value computes the combined value of all holdings owned by the portfolio
        Returns: double value
        """
        value = 0.0
        holdings = Holding.objects.filter(portfolio=self)
        for holding in holdings:
            value += holding.market_value()
        return value

    def compute_total_value(self):
        """
        compute_total_value computes the total value of the portfolio (cash + equities)
        Returns: N/A
        """
        self.total_value = self.equity_value() + float(self.cash_balance)
        self.save()

    def add_transaction(self, ticker, shares, price, transaction_type):
        """
        add_transaction creates a transaction record for a transaction that has occurred
        Returns: N/A
        """
        transaction = Transaction.objects.create()
        transaction.portfolio = self
        transaction.ticker = ticker
        transaction.trade_type = transaction_type
        transaction.shares = shares
        transaction.bought_price = price
        transaction.save()

    def buy_holding(self, ticker, shares):
        """
        buy_holding allows a user to purchase s shares of ticker t to add to the portfolio
        Returns: N/A or Exception if user cannot purchase s shares of ticker t
        """
        holding, created = Holding.objects.get_or_create(portfolio=self, ticker=ticker)
        price = holding.ask_price()
        if price is None:
            error = f"Ticker {ticker} is not currently traded."
            print(error)
            raise Exception(error)
        cost = price * float(shares)
        if float(self.cash_balance) < cost:
            error = f"Not enough cash to buy ${cost} in {shares} shares of {ticker}."
            print(error)
            raise Exception(error)
        holding.shares = float(0 if holding.shares is None else holding.shares) + float(
            shares
        )
        holding.save()

        self.cash_balance = float(self.cash_balance) - cost
        self.save()

        self.add_transaction(ticker, shares, price, TRANSACTION_TYPE_BUY)

    def sell_holding(self, ticker, shares):
        """
        sell_holding allows a user to sell s shares of ticker t currently in their portfolio
        Returns: N/A or Exception if user cannot sell s shares of ticker t
        """
        try:
            holding = Holding.objects.get(portfolio=self, ticker=ticker)
        except Holding.DoesNotExist:
            error = f"Holding {ticker} is not in portfolio."
            print(error)
            raise Exception(error)
        price = holding.bid_price()
        if price is None:
            error = f"Ticker {ticker} is not currently traded."
            print(error)
            raise Exception(error)
        current_shares = float(0 if holding.shares is None else holding.shares)
        if current_shares < float(shares):
            error = f"Not enough shares of {ticker} to sell {shares} shares."
            print(error)
            raise Exception(error)
        holding.shares = current_shares - float(shares)
        if holding.shares == 0.0:
            holding.delete()
        else:
            holding.save()

        self.cash_balance = float(self.cash_balance) + (price * float(shares))
        self.save()

        self.add_transaction(ticker, shares, price, TRANSACTION_TYPE_SELL)


class Holding(models.Model):
    """
    Holding represents a particular entity included in a portfolio
    """

    # Each holding associated with a portfolio
    portfolio = models.ForeignKey(
        Portfolio, null=True, blank=True, on_delete=models.CASCADE
    )
    ticker = models.TextField(max_length=5)
    shares = models.DecimalField(
        max_digits=14, decimal_places=2, default=0.00, null=True
    )
    created_on = models.DateTimeField(auto_now_add=True)
    uid = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    def __str__(self):
        """
        String representation of holding
        """
        return self.ticker

    def ask_price(self):
        """
        ask_price calls the yfinance API to compute the immediate price of the equity
        Returns: price of stock
        """
        tick = Ticker(str(self.ticker))
        stock_info = tick.info
        if stock_info.get("ask") is None:
            return None
        # Based on yfinance API restrictions to market hours, we return regularMarketPrice if after market hours
        if stock_info.get("ask") == 0:
            return stock_info.get("regularMarketPrice")
        return stock_info.get("ask")

    def bid_price(self):
        """
        bid_price calls the yfinance API to compute the immediate price of the equity
        Returns: price of stock
        """
        stock_info = Ticker(str(self.ticker)).info
        if stock_info.get("bid") is None:
            return None
        # Based on yfinance API restrictions to market hours, we return regularMarketPrice if after market hours
        if stock_info.get("bid") == 0:
            return stock_info.get("regularMarketPrice")
        return stock_info.get("bid")

    def market_value(self):
        """
        market_value computes market value of a holding
        Returns: double value
        """
        return self.bid_price() * float(self.shares)


class Transaction(models.Model):
    """
    Transactions are created every time a holding is purchased or sold
    """

    # Transactions are associated with certain portfolios
    portfolio = models.ForeignKey(
        Portfolio, null=True, blank=True, on_delete=models.CASCADE
    )
    ticker = models.TextField(max_length=200)
    trade_type = models.TextField(max_length=200)
    shares = models.DecimalField(
        max_digits=14, decimal_places=2, default=0.00, null=True
    )
    # Price that a holding was purchased/sold for
    bought_price = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)
    created_on = models.DateTimeField(auto_now_add=True)
    uid = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    def __str__(self):
        """
        String representation of transaction
        """
        return self.ticker
