from django.db import models
from django.contrib.auth.models import User
import uuid
import re
from datetime import datetime
from decimal import Decimal
from yfinance import Ticker

TRANSACTION_TYPE_BUY = "BUY"
TRANSACTION_TYPE_SELL = "SELL"
OPTION_TYPE_CALL = " CALL"
OPTION_TYPE_PUT = " PUT"
REGULAR_SHARES = 100.0


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
    rules = models.TextField(max_length=200, null=True, blank=True)
    # Winner is set once a user has won the game at the conclusion of the game
    winner = models.CharField(max_length=200, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    uid = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    class Meta:
        ordering = ['-created_on']

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
        ordering = ['-created_on']

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

    def validate_exercise(self, ticker, shares, price, contract, option_type):
        """
        validate_exercise makes sure that contract c can be exercised to buy/sell s shares of ticker t
        Returns: Option option or Exception if user cannot exercise c to buy/sell s shares of ticker t
        """
        if option_type == 'C':
            option_type_text = "call"
            flip = 1.0
        elif option_type == 'P':
            option_type_text = "put"
            flip = -1.0
        try:
            option = Option.objects.get(portfolio=self, contract=contract)
        except Option.DoesNotExist:
            error = f"Option {contract} is not in portfolio."
            print(error)
            raise Exception(error)
        if option.ticker() != ticker:
            error = f"Option {contract} is not for stock {ticker}."
            print(error)
            raise Exception(error)
        if option.expiration() <= datetime.now():
            error = f"Option {contract} has expired."
            print(error)
            raise Exception(error)
        if option.option_type() != option_type:
            error = f"Option {contract} is not a {option_type_text} option."
            print(error)
            raise Exception(error)
        if float(option.quantity) * REGULAR_SHARES < shares:
            error = f"Not enough shares available in option {contract}."
            print(error)
            raise Exception(error)
        if flip * option.strike_price() >= flip * price:
            warning = f"Warning: {option_type_text} option {contract} has a strike price of \
                        {option.strike_price()}. Current price of {ticker} is {price}."
            print(warning)
        return option

    def buy_holding(self, ticker, shares, exercise=None):
        """
        buy_holding allows a user to purchase s shares of ticker t to add to the portfolio
        Returns: N/A or Exception if user cannot purchase s shares of ticker t
        """
        holding, created = Holding.objects.get_or_create(portfolio=self, ticker=ticker)
        price = holding.ask_price()
        if price is None:
            if created:
                holding.delete()
            error = f"Ticker {ticker} is not currently traded."
            print(error)
            raise Exception(error)

        # If a call option is being exercised, make sure it is valid and compute cost accordingly
        if exercise:
            option = self.validate_exercise(ticker, shares, price, exercise, 'C')
            price = option.strike_price()
        cost = price * float(shares)

        if float(self.cash_balance) < cost:
            error = f"Not enough cash to buy ${cost} in {shares} shares of {ticker}."
            if created:
                holding.delete()
            print(error)
            raise Exception(error)
        holding.shares = float(0 if holding.shares is None else holding.shares) + float(
            shares
        )
        holding.save()
        self.cash_balance = float(self.cash_balance) - cost
        self.save()

        # If a call option was exercised, deduct shares from that option
        if exercise and option:
            option.quantity -= Decimal(shares / REGULAR_SHARES)
            option.save()

        self.add_transaction(ticker, shares, price, TRANSACTION_TYPE_BUY)

    def sell_holding(self, ticker, shares, exercise=None):
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

        # If a put option is being exercised, make sure it is valid and compute cost accordingly
        if exercise:
            option = self.validate_exercise(ticker, shares, price, exercise, 'P')
            price = option.strike_price()
        cost = price * float(shares)

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
        self.cash_balance = float(self.cash_balance) + cost
        self.save()

        # If a put option was exercised, deduct shares from that option
        if exercise and option:
            option.quantity -= Decimal(shares / REGULAR_SHARES)
            option.save()

        self.add_transaction(ticker, shares, price, TRANSACTION_TYPE_SELL)

    def buy_option(self, contract, quantity):
        """
        buy_option allows a user to purchase <quantity> options of contract name <contract>
        Returns: N/A or Exception if user cannot purchase specified quantity of said option
        """
        option, created = Option.objects.get_or_create(portfolio=self, contract=contract)
        price = option.ask_price()
        if price is None:
            if created:
                option.delete()
            error = f"Contract {contract} is not currently available."
            print(error)
            raise Exception(error)
        cost = price * float(quantity)
        if float(self.cash_balance) < cost:
            error = f"Not enough cash to buy ${cost} in {quantity} options of {contract}."
            if created:
                option.delete()
            print(error)
            raise Exception(error)
        option.quantity = float(0 if option.quantity is None else option.quantity) + float(
            quantity
        )
        option.save()

        self.cash_balance = float(self.cash_balance) - cost
        self.save()

        if option.option_type() == 'C':
            self.add_transaction(contract, quantity, price, TRANSACTION_TYPE_BUY + OPTION_TYPE_CALL)
        elif option.option_type() == 'P':
            self.add_transaction(contract, quantity, price, TRANSACTION_TYPE_BUY + OPTION_TYPE_PUT)

    def sell_option(self, contract, quantity):
        """
        sell_option allows a user to sell <quantity> options of contract name <contract> from portfolio
        Returns: N/A or Exception if user cannot sell specified quantity of said option
        """
        try:
            option = Option.objects.get(portfolio=self, contract=contract)
        except Option.DoesNotExist:
            error = f"Contract {contract} is not in portfolio."
            print(error)
            raise Exception(error)
        price = option.bid_price()
        if price is None:
            error = f"Contract {contract} is not currently available."
            print(error)
            raise Exception(error)
        current_quantity = float(0 if option.quantity is None else option.quantity)
        if current_quantity < float(quantity):
            error = f"Not enough of {contract} in portfolio to sell {quantity} options."
            print(error)
            raise Exception(error)
        option.quantity = current_quantity - float(quantity)
        if option.quantity == 0.0:
            option.delete()
        else:
            option.save()

        self.cash_balance = float(self.cash_balance) + (price * float(quantity))
        self.save()

        if option.option_type() == 'C':
            self.add_transaction(contract, quantity, price, TRANSACTION_TYPE_SELL + OPTION_TYPE_CALL)
        elif option.option_type() == 'P':
            self.add_transaction(contract, quantity, price, TRANSACTION_TYPE_SELL + OPTION_TYPE_PUT)


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

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        """
        String representation of holding
        """
        return self.ticker

    def ask_price(self):
        """
        ask_price calls the yfinance API to get the immediate buy price of the equity
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
        bid_price calls the yfinance API to get the immediate sell price of the equity
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
        price = self.bid_price() or 0.0
        return price * float(self.shares)


class Option(models.Model):
    """
    Option represents the ability to buy or sell a stock at a specific
    price before a certain time
    """

    # Each option associated with a portfolio
    portfolio = models.ForeignKey(
        Portfolio, null=True, blank=True, on_delete=models.CASCADE
    )
    contract = models.TextField(max_length=25)
    quantity = models.DecimalField(
        max_digits=12, decimal_places=2, default=0.00, null=True
    )
    created_on = models.DateTimeField(auto_now_add=True)
    uid = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        """
        String representation of option
        """
        return self.contract

    def ticker(self):
        """
        Return the stock ticker that this option is for
        """
        return re.split(r'(\d+)', self.contract)[0]

    def expiration(self):
        """
        Return the expiration date of this option in datetime format
        """
        exp = re.split(r'(\d+)', self.contract)[1]
        try:
            return datetime(2000 + int(exp[0:2]), int(exp[2:4]), int(exp[4:6]), 0, 0)
        except ValueError:
            return None

    def option_type(self):
        """
        Return the type of option: 'C' for call, 'P' for put
        """
        return re.split(r'(\d+)', self.contract)[2]

    def strike_price(self):
        """
        Return the strike price of this option, derived from contract symbol
        """
        return float(re.split(r'(\d+)', self.contract)[3]) / 1000.0

    def get_info(self):
        """
        Calls the yfinance API to get information on a specific option contract
        Returns: dict with info on option contract
        """
        tick = Ticker(str(self.ticker()))
        if not self.expiration():
            return None
        expdate = str(self.expiration().date())
        df = tick.option_chain(date=expdate)
        if self.option_type() == 'C':
            options = df.calls.set_index('contractSymbol').T.to_dict()
        elif self.option_type() == 'P':
            options = df.puts.set_index('contractSymbol').T.to_dict()
        else:
            return None
        if self.contract not in options:
            return None
        return options.get(self.contract)

    def ask_price(self):
        """
        ask_price calls the yfinance API to get the immediate buy price of a contract
        Returns: price of contract (1 regular option is REGULAR_SHARES shares)
        """
        info = self.get_info()
        if not info:
            return None
        # Based on yfinance API restrictions to market hours, we return lastPrice if after market hours
        if float(info.get("ask")) == 0:
            return float(info.get("lastPrice")) * REGULAR_SHARES
        return float(info.get("ask")) * REGULAR_SHARES

    def bid_price(self):
        """
        bid_price calls the yfinance API to get the immediate sell price of a contract
        Returns: price of contract (1 regular option is REGULAR_SHARES shares)
        """
        info = self.get_info()
        if not info:
            return None
        # Based on yfinance API restrictions to market hours, we return lastPrice if after market hours
        if float(info.get("bid")) == 0:
            return float(info.get("lastPrice")) * REGULAR_SHARES
        return float(info.get("bid")) * REGULAR_SHARES


class Transaction(models.Model):
    """
    Transactions are created every time a holding is purchased or sold
    """

    # Transactions are associated with certain portfolios
    portfolio = models.ForeignKey(
        Portfolio, null=True, blank=True, on_delete=models.SET_NULL
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

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        """
        String representation of transaction
        """
        return self.ticker
