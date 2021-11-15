from django.test import TestCase
from . import Game, Portfolio, Holding, Transaction
from django.contrib.auth.models import User


class GameTestCase(TestCase):
    def setUp(self):
        Game.objects.create(title="Test Game", startingBalance=5000, rules="test rules")
        """
        for i in range(3):
            Portfolio.objects.create()
        """

    def test_rank_portfolios(self):
        """Portfolios for a game are correctly ordered"""
        # pass


class PortfolioTestCase(TestCase):
    def setUp(self):
        Game.objects.create(title="Test Game", rules="test rules")
        User.objects.create()  # TODO: fix user creation
        game_id = ""  # TODO: game id?
        Portfolio.objects.create(title="Test portfolio", game=game_id)

    def test_equity_value(self):
        """Test that equity_value is computed correctly for a portfolio"""
        # pass

    def test_compute_total_value(self):
        """Test that total value computes correct total value for a portfolio"""
        # this should test default as well as after several trades
        # pass

    def test_add_transaction(self):
        """Test that transaction is successfully created"""
        # pass

    def test_buy_holding_success(self):
        """Test that user is able to successfully buy a holding"""
        # pass

    def test_buy_holding_fails(self):
        """Test that a user is not able to buy a holding if not enough funds"""
        # pass

    def test_sell_holding_success(self):
        """Test that a user is able to sell a holding"""
        # pass

    def test_sell_holding_fail_invalid_number(self):
        """Test that a user is not able to sell a holding if they try to sell more than they have"""
        # pass

    def test_sell_holding_fail_no_holding(self):
        """Test that a user is not able to sell a holding if they don't have it"""
        # pass


class HoldingTestCase(TestCase):
    def setUp(self):
        Holding.objects.create()
        # Create game
        # Create portfolio
        # Create holding

    def test_ask_price(self):
        """Test fetching ask price succeeds"""
        # pass

    def test_bid_price(self):
        """Test fetching bid price succeeds"""
        # pass

    def market_value(self):
        """Test fetching market value succeeds"""
        # pass


class TransactionTestCase(TestCase):
    def setUp(self):
        # Create portfolio
        Transaction.objects.create(
            ticker="AAPL", trade_type="BUY", shares=1, bought_price=122.34
        )
