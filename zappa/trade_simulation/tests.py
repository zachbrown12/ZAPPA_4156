from django.test import TestCase
import mock
from .models import Game, Portfolio, Holding, Transaction
from django.contrib.auth.models import User


class GameTestCase(TestCase):
    def setUp(self):
        # Create game
        Game.objects.create(
            title="Test Game", starting_balance=5000, rules="test rules"
        )

    def test_rank_portfolios_tie(self):
        """
        Test that portfolios for a game are correctly ordered when all portfolios have the same value
        """
        game = Game.objects.all()[0]
        # Create portfolios for game
        for i in range(3):
            Portfolio.objects.create(title=f"Test Portfolio {i}", game=game)
        leaderboard = game.rank_portfolios()
        # Test that leaderboard rankings are as expected
        assert len(leaderboard) == 3
        assert (
            leaderboard[0].game_rank == 1
            and leaderboard[1].game_rank == 1
            and leaderboard[2].game_rank == 1
        )

    def test_rank_portfolios_no_tie(self):
        """
        Test that portfolios for a game are correctly ordered when portfolios have different values
        """
        game = Game.objects.all()[0]
        # Create portfolios for game
        for i in range(3):
            cash_balance = (i + 1) * 1000
            Portfolio.objects.create(
                title=f"Test Portfolio {i}", game=game, cash_balance=cash_balance
            )

        leaderboard = game.rank_portfolios()
        # Test that leaderboard rankings are as expected
        assert len(leaderboard) == 3
        assert leaderboard[0].game_rank == 1
        assert leaderboard[1].game_rank == 2
        assert leaderboard[2].game_rank == 3


class PortfolioTestCase(TestCase):
    def setUp(self):
        # Create game
        Game.objects.create(title="Test Game", rules="test rules")
        game = Game.objects.all()[0]
        # Create portfolio
        Portfolio.objects.create(title="Test portfolio", game=game)

    @mock.patch("trade_simulation.models.Holding.bid_price", return_value=200)
    def test_equity_value_success(self, mock_bid_price):
        """
        Test that equity_value is computed correctly for a portfolio
        """
        # Add initial holding to portfolio
        portfolio = Portfolio.objects.all()[0]
        Holding.objects.create(ticker="AAPL", shares=2, portfolio=portfolio)
        expected = 400
        actual = portfolio.equity_value()
        assert expected == actual

    def test_equity_value_no_holdings(self):
        """
        Test that equity_value is 0 when no holdings in portfolio
        """
        portfolio = Portfolio.objects.all()[0]
        expected = 0
        actual = portfolio.equity_value()
        assert expected == actual

    def test_compute_total_value_no_holdings(self):
        """
        Test that compute_total_value returns correct total value for a portfolio when there are no holdings
        """
        portfolio = Portfolio.objects.all()[0]
        expected = 10000
        portfolio.compute_total_value()
        actual = portfolio.total_value
        assert expected == actual

    @mock.patch("trade_simulation.models.Portfolio.equity_value", return_value=3000)
    def test_compute_total_value_success(self, mock_equity_value):
        """
        Test that compute_total_value returns correct total value for a portfolio with holdings
        """
        portfolio = Portfolio.objects.all()[0]
        # Create holdings
        Holding.objects.create(ticker="AAPL", shares=2, portfolio=portfolio)
        Holding.objects.create(ticker="TSLA", shares=3, portfolio=portfolio)
        expected = 13000
        portfolio.compute_total_value()
        actual = portfolio.total_value
        assert expected == actual

    def test_add_transaction(self):
        """
        Test that transaction is successfully created
        """
        portfolio = Portfolio.objects.all()[0]
        ticker = "AAPL"
        shares = 12
        price = 124.23
        transaction_type = "BUY"
        portfolio.add_transaction(ticker, shares, price, transaction_type)
        t = Transaction.objects.get(portfolio=portfolio)
        assert t.ticker == ticker
        assert t.shares == shares
        assert float(t.bought_price) == price
        assert t.trade_type == transaction_type

    @mock.patch("trade_simulation.models.Holding.ask_price", return_value=200)
    def test_buy_new_holding_success(self, mock_ask_price):
        """
        Test that user is able to successfully buy a holding
        """
        portfolio = Portfolio.objects.all()[0]
        ticker = "AAPL"
        shares = 1
        portfolio.buy_holding(ticker, shares)
        h = Holding.objects.get(portfolio=portfolio)
        assert h.ticker == ticker
        assert h.shares == shares
        t = Transaction.objects.get(portfolio=portfolio)
        assert t.ticker == ticker
        assert t.shares == shares
        assert float(t.bought_price) == mock_ask_price.return_value
        assert t.trade_type == "BUY"

    @mock.patch("trade_simulation.models.Holding.ask_price", return_value=200)
    def test_buy_existing_holding_success(self, mock_ask_price):
        """
        Test that user is able to successfully buy an existing holding
        """
        # Create initial holding
        portfolio = Portfolio.objects.all()[0]
        ticker = "AAPL"
        Holding.objects.create(ticker=ticker, shares=2, portfolio=portfolio)
        shares = 1
        # Buy a new share of the holding
        portfolio.buy_holding(ticker, shares)
        h = Holding.objects.get(portfolio=portfolio)
        assert h.ticker == ticker
        assert h.shares == shares + 2
        t = Transaction.objects.get(portfolio=portfolio)
        assert t.ticker == ticker
        assert t.shares == shares
        assert float(t.bought_price) == mock_ask_price.return_value
        assert t.trade_type == "BUY"

    @mock.patch("trade_simulation.models.Holding.ask_price", return_value=None)
    def test_buy_holding_fails_not_traded(self, mock_ask_price):
        """
        Test that a user is not able to buy a holding if ask price is None
        """
        portfolio = Portfolio.objects.all()[0]
        ticker = "AAPL"
        shares = 1
        with self.assertRaises(Exception) as e:
            portfolio.buy_holding(ticker, shares)
            self.assertIn(str(e.exception), f"Ticker {ticker} is not currently traded")

    @mock.patch("trade_simulation.models.Holding.ask_price", return_value=500)
    def test_buy_holding_fails_no_cash(self, mock_ask_price):
        """
        Test that a user is not able to buy a holding if ask price is None
        """
        portfolio = Portfolio.objects.all()[0]
        ticker = "AAPL"
        shares = 2000
        with self.assertRaises(Exception) as e:
            portfolio.buy_holding(ticker, shares)
            self.assertIn(str(e.exception), "Not enough cash to buy")

    @mock.patch("trade_simulation.models.Holding.bid_price", return_value=200)
    def test_sell_all_holding_success(self, mock_bid_price):
        """
        Test that a user is able to sell all shares of a holding
        """
        portfolio = Portfolio.objects.all()[0]
        ticker = "AAPL"
        shares = 2
        Holding.objects.create(ticker=ticker, shares=shares, portfolio=portfolio)
        portfolio.sell_holding(ticker, shares)
        with self.assertRaises(Holding.DoesNotExist):
            Holding.objects.get(portfolio=portfolio)
        t = Transaction.objects.get(portfolio=portfolio)
        assert t.ticker == ticker
        assert t.shares == shares
        assert float(t.bought_price) == mock_bid_price.return_value
        assert t.trade_type == "SELL"
        assert portfolio.cash_balance == 10000 + (shares * mock_bid_price.return_value)

    @mock.patch("trade_simulation.models.Holding.bid_price", return_value=200)
    def test_sell_holding_success(self, mock_bid_price):
        """
        Test that a user is able to sell some shares of a holding
        And still has some leftover
        """
        portfolio = Portfolio.objects.all()[0]
        ticker = "AAPL"
        shares = 2
        Holding.objects.create(ticker=ticker, shares=3, portfolio=portfolio)
        portfolio.sell_holding(ticker, shares)
        h = Holding.objects.get(portfolio=portfolio)
        assert h.shares == 1
        assert h.ticker == ticker
        t = Transaction.objects.get(portfolio=portfolio)
        assert t.ticker == ticker
        assert t.shares == shares
        assert float(t.bought_price) == mock_bid_price.return_value
        assert t.trade_type == "SELL"
        assert portfolio.cash_balance == 10000 + (shares * mock_bid_price.return_value)

    @mock.patch("trade_simulation.models.Holding.bid_price", return_value=200)
    def test_sell_holding_fail_invalid_number(self, mock_bid_price):
        """
        Test that a user is not able to sell a holding if they try to sell more shares than they have
        """
        portfolio = Portfolio.objects.all()[0]
        ticker = "AAPL"
        shares = 3
        Holding.objects.create(ticker=ticker, shares=shares, portfolio=portfolio)
        with self.assertRaises(Exception) as e:
            portfolio.sell_holding(ticker, shares + 1)
            self.assertIn(str(e.exception), "Not enough shares")

    def test_sell_holding_fail_no_holding(self):
        """
        Test that a user is not able to sell a holding if they don't have it
        """
        portfolio = Portfolio.objects.all()[0]
        ticker = "AAPL"
        shares = 1
        with self.assertRaises(Exception) as e:
            portfolio.sell_holding(ticker, shares)
            self.assertIn(str(e.exception), f"Holding {ticker} is not in portfolio.")

    @mock.patch("trade_simulation.models.Holding.bid_price", return_value=None)
    def test_sell_holding_fail_not_traded(self, mock_bid_price):
        """
        Test that a user is not able to sell a holding if it's not currently traded
        """
        portfolio = Portfolio.objects.all()[0]
        ticker = "AAPL"
        shares = 1
        Holding.objects.create(ticker=ticker, shares=shares, portfolio=portfolio)
        with self.assertRaises(Exception) as e:
            portfolio.sell_holding(ticker, shares)
            self.assertIn(str(e.exception), f"Ticker {ticker} is not currently traded.")


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
