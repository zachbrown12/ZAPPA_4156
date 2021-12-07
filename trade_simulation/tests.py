from datetime import datetime
from django.test import TestCase
import unittest.mock as mock
from unittest.mock import PropertyMock
from .models import Game, Portfolio, Holding, Option, Transaction
from django.contrib.auth.models import User
from pandas import DataFrame
from types import SimpleNamespace


class GameTestCase(TestCase):
    def setUp(self):
        # Create game
        Game.objects.create(
            title="Test Game", starting_balance=5000, rules="test rules"
        )

    def test_str(self):
        """
        Test __str__() returns title
        """
        # GIVEN
        g = Game.objects.all()[0]
        # WHEN / THEN
        assert g.__str__() == "Test Game"

    def test_rank_portfolios_tie(self):
        """
        Test that portfolios for a game are correctly ordered when all portfolios have the same value
        """
        # GIVEN
        game = Game.objects.all()[0]
        # Create portfolios for game
        for i in range(3):
            Portfolio.objects.create(title=f"Test Portfolio {i}", game=game)
        # WHEN
        leaderboard = game.rank_portfolios()
        # Test that leaderboard rankings are as expected
        # THEN
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
        # GIVEN
        game = Game.objects.all()[0]
        # Create portfolios for game
        for i in range(3):
            cash_balance = (i + 1) * 1000
            Portfolio.objects.create(
                title=f"Test Portfolio {i}", game=game, cash_balance=cash_balance
            )

        # WHEN
        leaderboard = game.rank_portfolios()
        # Test that leaderboard rankings are as expected
        # THEN
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

    def test_str(self):
        """
        Test __str__() returns title
        """
        # GIVEN
        p = Portfolio.objects.all()[0]
        # WHEN / THEN
        assert p.__str__() == "Test portfolio"

    @mock.patch("trade_simulation.models.Holding.bid_price", return_value=200)
    def test_equity_value_success(self, mock_bid_price):
        """
        Test that equity_value is computed correctly for a portfolio
        """
        # GIVEN
        # Add initial holding to portfolio
        portfolio = Portfolio.objects.all()[0]
        Holding.objects.create(ticker="AAPL", shares=2, portfolio=portfolio)
        Option.objects.create(contract="AAPL211223C00148000", quantity=1, portfolio=portfolio)
        expected = 400
        # WHEN
        actual = portfolio.equity_value()
        # THEN
        assert expected == actual

    def test_equity_value_options_only(self):
        """
        Test that equity_value is 0 when only options in portfolio
        """
        # GIVEN
        portfolio = Portfolio.objects.all()[0]
        Option.objects.create(contract="AAPL211223C00148000", quantity=2, portfolio=portfolio)
        Option.objects.create(contract="TSLA211231P01115000", quantity=3, portfolio=portfolio)
        expected = 0
        # WHEN
        actual = portfolio.equity_value()
        # THEN
        assert expected == actual

    def test_equity_value_no_holdings(self):
        """
        Test that equity_value is 0 when no holdings in portfolio
        """
        # GIVEN
        portfolio = Portfolio.objects.all()[0]
        expected = 0
        # WHEN
        actual = portfolio.equity_value()
        # THEN
        assert expected == actual

    def test_compute_total_value_no_holdings(self):
        """
        Test that compute_total_value returns correct total value for a portfolio when there are no holdings
        """
        # GIVEN
        portfolio = Portfolio.objects.all()[0]
        expected = 10000
        # WHEN
        portfolio.compute_total_value()
        actual = portfolio.total_value
        # THEN
        assert expected == actual

    @mock.patch("trade_simulation.models.Portfolio.equity_value", return_value=3000)
    def test_compute_total_value_success(self, mock_equity_value):
        """
        Test that compute_total_value returns correct total value for a portfolio with holdings
        """
        # GIVEN
        portfolio = Portfolio.objects.all()[0]
        # Create holdings
        Holding.objects.create(ticker="AAPL", shares=2, portfolio=portfolio)
        Holding.objects.create(ticker="TSLA", shares=3, portfolio=portfolio)
        Option.objects.create(contract="AAPL211223C00148000", quantity=2, portfolio=portfolio)
        expected = 13000
        # WHEN
        portfolio.compute_total_value()
        actual = portfolio.total_value
        # THEN
        assert expected == actual

    def test_add_transaction(self):
        """
        Test that transaction is successfully created
        """
        # GIVEN
        portfolio = Portfolio.objects.all()[0]
        ticker = "AAPL"
        shares = 12
        price = 124.23
        transaction_type = "BUY"
        # WHEN
        portfolio.add_transaction(ticker, shares, price, transaction_type)
        t = Transaction.objects.get(portfolio=portfolio)
        # THEN
        assert t.ticker == ticker
        assert t.shares == shares
        assert float(t.bought_price) == price
        assert t.trade_type == transaction_type

    @mock.patch("trade_simulation.models.Holding.ask_price", return_value=200)
    def test_buy_new_holding_success(self, mock_ask_price):
        """
        Test that user is able to successfully buy a holding
        """
        # GIVEN
        portfolio = Portfolio.objects.all()[0]
        ticker = "AAPL"
        shares = 1
        # WHEN
        portfolio.buy_holding(ticker, shares)
        h = Holding.objects.get(portfolio=portfolio)
        # THEN
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
        # GIVEN
        portfolio = Portfolio.objects.all()[0]
        ticker = "AAPL"
        Holding.objects.create(ticker=ticker, shares=2, portfolio=portfolio)
        shares = 1
        # WHEN
        portfolio.buy_holding(ticker, shares)
        h = Holding.objects.get(portfolio=portfolio)
        # THEN
        assert h.ticker == ticker
        assert h.shares == shares + 2
        t = Transaction.objects.get(portfolio=portfolio)
        assert t.ticker == ticker
        assert t.shares == shares
        assert float(t.bought_price) == mock_ask_price.return_value
        assert t.trade_type == "BUY"

    @mock.patch("trade_simulation.models.Holding.ask_price", return_value=200)
    def test_buy_new_holding_with_option_success(self, mock_ask_price):
        """
        Test that user is able to successfully buy a holding while exercising a call option
        """
        # GIVEN
        portfolio = Portfolio.objects.all()[0]
        contract = "AAPL211223C00148000"
        quantity = 1
        Option.objects.create(contract=contract, quantity=quantity, portfolio=portfolio)
        ticker = "AAPL"
        shares = 1
        # WHEN
        portfolio.buy_holding(ticker, shares, exercise=contract)
        h = Holding.objects.get(portfolio=portfolio)
        # THEN
        assert h.ticker == ticker
        assert h.shares == shares
        t = Transaction.objects.get(portfolio=portfolio)
        assert t.ticker == ticker
        assert t.shares == shares
        assert float(t.bought_price) == 148.0
        assert t.trade_type == "BUY"

    @mock.patch("trade_simulation.models.Holding.ask_price", return_value=200)
    def test_buy_new_holding_with_option_missing_option(self, mock_ask_price):
        """
        Test that user cannot exercise a call option not in portfolio
        """
        # GIVEN
        portfolio = Portfolio.objects.all()[0]
        contract = "AAPL211223C00148000"
        ticker = "AAPL"
        shares = 1
        # WHEN/THEN
        with self.assertRaises(Exception) as e:
            portfolio.buy_holding(ticker, shares, exercise=contract)
            self.assertIn(str(e.exception), f"Option {contract} is not in portfolio.")

    @mock.patch("trade_simulation.models.Holding.ask_price", return_value=200)
    def test_buy_new_holding_with_option_mismatch(self, mock_ask_price):
        """
        Test that user cannot exercise a call option that doesn't match the stock being bought
        """
        # GIVEN
        portfolio = Portfolio.objects.all()[0]
        contract = "TSLA211231P01115000"
        quantity = 1
        Option.objects.create(contract=contract, quantity=quantity, portfolio=portfolio)
        ticker = "AAPL"
        shares = 1
        # WHEN/THEN
        with self.assertRaises(Exception) as e:
            portfolio.buy_holding(ticker, shares, exercise=contract)
            self.assertIn(str(e.exception), "Option {contract} is not for stock {ticker}.")

    @mock.patch("trade_simulation.models.Holding.ask_price", return_value=200)
    def test_buy_new_holding_with_option_expired(self, mock_ask_price):
        """
        Test that user cannot exercise a call option that has expired
        """
        # GIVEN
        portfolio = Portfolio.objects.all()[0]
        contract = "AAPL201223C00148000"
        quantity = 1
        Option.objects.create(contract=contract, quantity=quantity, portfolio=portfolio)
        ticker = "AAPL"
        shares = 1
        # WHEN/THEN
        with self.assertRaises(Exception) as e:
            portfolio.buy_holding(ticker, shares, exercise=contract)
            self.assertIn(str(e.exception), "Option {contract} has expired.")

    @mock.patch("trade_simulation.models.Holding.ask_price", return_value=None)
    def test_buy_holding_fails_not_traded(self, mock_ask_price):
        """
        Test that a user is not able to buy a holding if ask price is None
        """
        # GIVEN
        portfolio = Portfolio.objects.all()[0]
        ticker = "AAPL"
        shares = 1
        # WHEN / THEN
        with self.assertRaises(Exception) as e:
            portfolio.buy_holding(ticker, shares)
            self.assertIn(str(e.exception), f"Ticker {ticker} is not currently traded")

    @mock.patch("trade_simulation.models.Holding.ask_price", return_value=500)
    def test_buy_holding_fails_no_cash(self, mock_ask_price):
        """
        Test that a user is not able to buy a holding with not enough cash
        """
        # GIVEN
        portfolio = Portfolio.objects.all()[0]
        ticker = "AAPL"
        shares = 2000
        # WHEN / THEN
        with self.assertRaises(Exception) as e:
            portfolio.buy_holding(ticker, shares)
            self.assertIn(str(e.exception), "Not enough cash to buy")

    @mock.patch("trade_simulation.models.Holding.bid_price", return_value=200)
    def test_sell_all_holding_success(self, mock_bid_price):
        """
        Test that a user is able to sell all shares of a holding
        """
        # GIVEN
        portfolio = Portfolio.objects.all()[0]
        ticker = "AAPL"
        shares = 2
        Holding.objects.create(ticker=ticker, shares=shares, portfolio=portfolio)
        # WHEN
        portfolio.sell_holding(ticker, shares)
        # THEN
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
        # GIVEN
        portfolio = Portfolio.objects.all()[0]
        ticker = "AAPL"
        shares = 2
        Holding.objects.create(ticker=ticker, shares=3, portfolio=portfolio)
        # WHEN
        portfolio.sell_holding(ticker, shares)
        h = Holding.objects.get(portfolio=portfolio)
        # THEN
        assert h.shares == 1
        assert h.ticker == ticker
        t = Transaction.objects.get(portfolio=portfolio)
        assert t.ticker == ticker
        assert t.shares == shares
        assert float(t.bought_price) == mock_bid_price.return_value
        assert t.trade_type == "SELL"
        assert portfolio.cash_balance == 10000 + (shares * mock_bid_price.return_value)

    @mock.patch("trade_simulation.models.Holding.bid_price", return_value=1000)
    def test_sell_holding_with_option_success(self, mock_bid_price):
        """
        Test that a user is able to sell some shares of a holding while exercising a put option
        """
        # GIVEN
        portfolio = Portfolio.objects.all()[0]
        contract = "TSLA211231P01115000"
        quantity = 1
        Option.objects.create(contract=contract, quantity=quantity, portfolio=portfolio)
        ticker = "TSLA"
        shares = 2
        Holding.objects.create(ticker=ticker, shares=3, portfolio=portfolio)
        # WHEN
        portfolio.sell_holding(ticker, shares, exercise=contract)
        h = Holding.objects.get(portfolio=portfolio)
        # THEN
        assert h.shares == 1
        assert h.ticker == ticker
        t = Transaction.objects.get(portfolio=portfolio)
        assert t.ticker == ticker
        assert t.shares == shares
        print(t.bought_price)
        assert float(t.bought_price) == 1115.0
        assert t.trade_type == "SELL"
        assert portfolio.cash_balance == 10000 + (shares * 1115.0)

    @mock.patch("trade_simulation.models.Holding.bid_price", return_value=1000)
    def test_sell_holding_with_option_wrong_type(self, mock_bid_price):
        """
        Test that a user is not able to sell a holding while exercising a call option
        """
        # GIVEN
        portfolio = Portfolio.objects.all()[0]
        contract = "TSLA211231C01115000"
        quantity = 1
        Option.objects.create(contract=contract, quantity=quantity, portfolio=portfolio)
        ticker = "TSLA"
        shares = 2
        Holding.objects.create(ticker=ticker, shares=3, portfolio=portfolio)
        # WHEN/THEN
        with self.assertRaises(Exception) as e:
            portfolio.sell_holding(ticker, shares, exercise=contract)
            self.assertIn(str(e.exception), f"Option {contract} is not a put option.")

    @mock.patch("trade_simulation.models.Holding.bid_price", return_value=1000)
    def test_sell_holding_with_option_insufficient_quantity(self, mock_bid_price):
        """
        Test that a user is not able to sell a holding while exercising an option with too few shares
        """
        # GIVEN
        portfolio = Portfolio.objects.all()[0]
        contract = "TSLA211231P01115000"
        quantity = 0.01
        Option.objects.create(contract=contract, quantity=quantity, portfolio=portfolio)
        ticker = "TSLA"
        shares = 2
        Holding.objects.create(ticker=ticker, shares=3, portfolio=portfolio)
        # WHEN/THEN
        with self.assertRaises(Exception) as e:
            portfolio.sell_holding(ticker, shares, exercise=contract)
            self.assertIn(str(e.exception), "Not enough shares available in option")

    @mock.patch("trade_simulation.models.Holding.bid_price", return_value=200)
    def test_sell_holding_fail_invalid_number(self, mock_bid_price):
        """
        Test that a user is not able to sell a holding if they try to sell more shares than they have
        """
        # GIVEN
        portfolio = Portfolio.objects.all()[0]
        ticker = "AAPL"
        shares = 3
        Holding.objects.create(ticker=ticker, shares=shares, portfolio=portfolio)
        # WHEN / THEN
        with self.assertRaises(Exception) as e:
            portfolio.sell_holding(ticker, shares + 1)
            self.assertIn(str(e.exception), "Not enough shares")

    def test_sell_holding_fail_no_holding(self):
        """
        Test that a user is not able to sell a holding if they don't have it
        """
        # GIVEN
        portfolio = Portfolio.objects.all()[0]
        ticker = "AAPL"
        shares = 1
        # WHEN / THEN
        with self.assertRaises(Exception) as e:
            portfolio.sell_holding(ticker, shares)
            self.assertIn(str(e.exception), f"Holding {ticker} is not in portfolio.")

    @mock.patch("trade_simulation.models.Holding.bid_price", return_value=None)
    def test_sell_holding_fail_not_traded(self, mock_bid_price):
        """
        Test that a user is not able to sell a holding if it's not currently traded
        """
        # GIVEN
        portfolio = Portfolio.objects.all()[0]
        ticker = "AAPL"
        shares = 1
        Holding.objects.create(ticker=ticker, shares=shares, portfolio=portfolio)
        # WHEN / THEN
        with self.assertRaises(Exception) as e:
            portfolio.sell_holding(ticker, shares)
            self.assertIn(str(e.exception), f"Ticker {ticker} is not currently traded.")

    @mock.patch("trade_simulation.models.Option.ask_price", return_value=2000)
    def test_buy_new_call_option_success(self, mock_ask_price):
        """
        Test that user is able to successfully buy a call option
        """
        # GIVEN
        portfolio = Portfolio.objects.all()[0]
        contract = "AAPL211223C00148000"
        quantity = 2
        # WHEN
        portfolio.buy_option(contract, quantity)
        opt = Option.objects.get(portfolio=portfolio)
        # THEN
        assert opt.contract == contract
        assert opt.quantity == quantity
        t = Transaction.objects.get(portfolio=portfolio)
        # THEN
        assert t.ticker == contract
        assert t.shares == quantity
        assert float(t.bought_price) == mock_ask_price.return_value
        assert t.trade_type == "BUY CALL"

    @mock.patch("trade_simulation.models.Option.ask_price", return_value=9000)
    def test_buy_new_put_option_success(self, mock_ask_price):
        """
        Test that user is able to successfully buy a put option
        """
        # GIVEN
        portfolio = Portfolio.objects.all()[0]
        contract = "TSLA211231P01115000"
        quantity = 1
        # WHEN
        portfolio.buy_option(contract, quantity)
        opt = Option.objects.get(portfolio=portfolio)
        # THEN
        assert opt.contract == contract
        assert opt.quantity == quantity
        t = Transaction.objects.get(portfolio=portfolio)
        # THEN
        assert t.ticker == contract
        assert t.shares == quantity
        assert float(t.bought_price) == mock_ask_price.return_value
        assert t.trade_type == "BUY PUT"

    @mock.patch("trade_simulation.models.Option.ask_price", return_value=2000)
    def test_buy_existing_call_option_success(self, mock_ask_price):
        """
        Test that user is able to successfully buy an existing call option
        """
        # GIVEN
        portfolio = Portfolio.objects.all()[0]
        contract = "AAPL211223C00148000"
        Option.objects.create(contract=contract, quantity=2, portfolio=portfolio)
        quantity = 1
        # WHEN
        portfolio.buy_option(contract, quantity)
        opt = Option.objects.get(portfolio=portfolio)
        # THEN
        assert opt.contract == contract
        assert opt.quantity == quantity + 2
        t = Transaction.objects.get(portfolio=portfolio)
        # THEN
        assert t.ticker == contract
        assert t.shares == quantity
        assert float(t.bought_price) == mock_ask_price.return_value
        assert t.trade_type == "BUY CALL"

    @mock.patch("trade_simulation.models.Option.ask_price", return_value=9000)
    def test_buy_existing_put_option_success(self, mock_ask_price):
        """
        Test that user is able to successfully buy an existing put option
        """
        # GIVEN
        portfolio = Portfolio.objects.all()[0]
        contract = "TSLA211231P01115000"
        Option.objects.create(contract=contract, quantity=2, portfolio=portfolio)
        quantity = 1
        # WHEN
        portfolio.buy_option(contract, quantity)
        opt = Option.objects.get(portfolio=portfolio)
        # THEN
        assert opt.contract == contract
        assert opt.quantity == quantity + 2
        t = Transaction.objects.get(portfolio=portfolio)
        # THEN
        assert t.ticker == contract
        assert t.shares == quantity
        assert float(t.bought_price) == mock_ask_price.return_value
        assert t.trade_type == "BUY PUT"

    @mock.patch("trade_simulation.models.Option.ask_price", return_value=None)
    def test_buy_option_fails_not_traded(self, mock_ask_price):
        """
        Test that a user is not able to buy an option if ask price is None
        """
        # GIVEN
        portfolio = Portfolio.objects.all()[0]
        contract = "AAPL211223C00148000"
        quantity = 1
        # WHEN / THEN
        with self.assertRaises(Exception) as e:
            portfolio.buy_option(contract, quantity)
            self.assertIn(str(e.exception), f"Contract {contract} is not currently available.")

    @mock.patch("trade_simulation.models.Option.ask_price", return_value=15000)
    def test_buy_option_fails_no_cash(self, mock_ask_price):
        """
        Test that a user is not able to buy an option with not enough cash
        """
        # GIVEN
        portfolio = Portfolio.objects.all()[0]
        contract = "TSLA211231P01115000"
        quantity = 5
        # WHEN / THEN
        with self.assertRaises(Exception) as e:
            portfolio.buy_option(contract, quantity)
            self.assertIn(str(e.exception), "Not enough cash to buy")

    @mock.patch("trade_simulation.models.Option.bid_price", return_value=2000)
    def test_sell_all_call_option_success(self, mock_bid_price):
        """
        Test that a user is able to sell entire quantity of a call option
        """
        # GIVEN
        portfolio = Portfolio.objects.all()[0]
        contract = "AAPL211223C00148000"
        quantity = 2
        Option.objects.create(contract=contract, quantity=quantity, portfolio=portfolio)
        # WHEN
        portfolio.sell_option(contract, quantity)
        # THEN
        with self.assertRaises(Option.DoesNotExist):
            Option.objects.get(portfolio=portfolio)
        t = Transaction.objects.get(portfolio=portfolio)
        # THEN
        assert t.ticker == contract
        assert t.shares == quantity
        assert float(t.bought_price) == mock_bid_price.return_value
        assert t.trade_type == "SELL CALL"
        assert portfolio.cash_balance == 10000 + (quantity * mock_bid_price.return_value)

    @mock.patch("trade_simulation.models.Option.bid_price", return_value=9000)
    def test_sell_all_put_option_success(self, mock_bid_price):
        """
        Test that a user is able to sell entire quantity of a put option
        """
        # GIVEN
        portfolio = Portfolio.objects.all()[0]
        contract = "TSLA211231P01115000"
        quantity = 2
        Option.objects.create(contract=contract, quantity=quantity, portfolio=portfolio)
        # WHEN
        portfolio.sell_option(contract, quantity)
        # THEN
        with self.assertRaises(Option.DoesNotExist):
            Option.objects.get(portfolio=portfolio)
        t = Transaction.objects.get(portfolio=portfolio)
        # THEN
        assert t.ticker == contract
        assert t.shares == quantity
        assert float(t.bought_price) == mock_bid_price.return_value
        assert t.trade_type == "SELL PUT"
        assert portfolio.cash_balance == 10000 + (quantity * mock_bid_price.return_value)

    @mock.patch("trade_simulation.models.Option.bid_price", return_value=2000)
    def test_sell_call_option_success(self, mock_bid_price):
        """
        Test that a user is able to sell some shares of a call option
        And still have some leftover
        """
        # GIVEN
        portfolio = Portfolio.objects.all()[0]
        contract = "AAPL211223C00148000"
        quantity = 2
        Option.objects.create(contract=contract, quantity=3, portfolio=portfolio)
        # WHEN
        portfolio.sell_option(contract, quantity)
        opt = Option.objects.get(portfolio=portfolio)
        # THEN
        assert opt.quantity == 1
        assert opt.contract == contract
        t = Transaction.objects.get(portfolio=portfolio)
        # THEN
        assert t.ticker == contract
        assert t.shares == quantity
        assert float(t.bought_price) == mock_bid_price.return_value
        assert t.trade_type == "SELL CALL"
        assert portfolio.cash_balance == 10000 + (quantity * mock_bid_price.return_value)

    @mock.patch("trade_simulation.models.Option.bid_price", return_value=9000)
    def test_sell_put_option_success(self, mock_bid_price):
        """
        Test that a user is able to sell some shares of a put option
        And still have some leftover
        """
        # GIVEN
        portfolio = Portfolio.objects.all()[0]
        contract = "TSLA211231P01115000"
        quantity = 2
        Option.objects.create(contract=contract, quantity=3, portfolio=portfolio)
        # WHEN
        portfolio.sell_option(contract, quantity)
        opt = Option.objects.get(portfolio=portfolio)
        # THEN
        assert opt.quantity == 1
        assert opt.contract == contract
        t = Transaction.objects.get(portfolio=portfolio)
        # THEN
        assert t.ticker == contract
        assert t.shares == quantity
        assert float(t.bought_price) == mock_bid_price.return_value
        assert t.trade_type == "SELL PUT"
        assert portfolio.cash_balance == 10000 + (quantity * mock_bid_price.return_value)

    @mock.patch("trade_simulation.models.Option.bid_price", return_value=2000)
    def test_sell_option_fail_invalid_number(self, mock_bid_price):
        """
        Test that a user is not able to sell an option if they try to sell more of it than they have
        """
        # GIVEN
        portfolio = Portfolio.objects.all()[0]
        contract = "AAPL211223C00148000"
        quantity = 3
        Option.objects.create(contract=contract, quantity=quantity, portfolio=portfolio)
        # WHEN / THEN
        with self.assertRaises(Exception) as e:
            portfolio.sell_option(contract, quantity + 1)
            self.assertIn(str(e.exception), "Not enough of")

    def test_sell_option_fail_no_option(self):
        """
        Test that a user is not able to sell an option if they don't have it
        """
        # GIVEN
        portfolio = Portfolio.objects.all()[0]
        contract = "AAPL211223C00148000"
        quantity = 1
        # WHEN / THEN
        with self.assertRaises(Exception) as e:
            portfolio.sell_option(contract, quantity)
            self.assertIn(str(e.exception), f"Contract {contract} is not in portfolio.")

    @mock.patch("trade_simulation.models.Option.bid_price", return_value=None)
    def test_sell_option_fail_not_traded(self, mock_bid_price):
        """
        Test that a user is not able to sell an option if it's not currently traded
        """
        # GIVEN
        portfolio = Portfolio.objects.all()[0]
        contract = "AAPX211223C00148000"
        quantity = 1
        Option.objects.create(contract=contract, quantity=quantity, portfolio=portfolio)
        # WHEN / THEN
        with self.assertRaises(Exception) as e:
            portfolio.sell_option(contract, quantity)
            self.assertIn(str(e.exception), f"Contract {contract} is not currently available.")


class HoldingTestCase(TestCase):
    def setUp(self):
        # Create game
        Game.objects.create(title="Test Game", rules="test rules")
        game = Game.objects.all()[0]
        # Create portfolio
        Portfolio.objects.create(title="Test portfolio", game=game)
        # Create holding
        portfolio = Portfolio.objects.all()[0]
        Holding.objects.create(portfolio=portfolio, ticker="AAPL", shares=3)

    def test_str(self):
        """
        Test __str__() returns ticker
        """
        # GIVEN
        h = Holding.objects.all()[0]
        # WHEN / THEN
        assert h.__str__() == "AAPL"

    @mock.patch("yfinance.Ticker.info", new_callable=PropertyMock)
    def test_ask_price_success(self, mock_ticker):
        """
        Test fetching ask price succeeds
        """
        # GIVEN
        test_ask = 123.23
        mock_ticker.return_value = {"ask": test_ask}
        holding = Holding.objects.all()[0]
        # WHEN
        actual = holding.ask_price()
        # THEN
        assert test_ask == actual

    @mock.patch("yfinance.Ticker.info", new_callable=PropertyMock)
    def test_ask_price_regular_market(self, mock_ticker):
        """
        Test that regularMarketPrice is returned if ask price is 0
        """
        # GIVEN
        test_ask = 0
        regular_market_price = 42.22
        mock_ticker.return_value = {
            "ask": test_ask,
            "regularMarketPrice": regular_market_price,
        }
        holding = Holding.objects.all()[0]
        # WHEN
        actual = holding.ask_price()
        # THEN
        assert regular_market_price == actual

    @mock.patch("yfinance.Ticker.info", new_callable=PropertyMock)
    def test_ask_price_none(self, mock_ticker):
        """
        Test that if ask is not present in stock info, None is returned
        """
        # GIVEN
        mock_ticker.return_value = {}
        holding = Holding.objects.all()[0]
        # WHEN
        actual = holding.ask_price()
        # THEN
        assert actual is None

    @mock.patch("yfinance.Ticker.info", new_callable=PropertyMock)
    def test_bid_price_success(self, mock_ticker):
        """
        Test fetching bid price succeeds
        """
        # GIVEN
        test_bid = 123.23
        mock_ticker.return_value = {"bid": test_bid}
        holding = Holding.objects.all()[0]
        # WHEN
        actual = holding.bid_price()
        # THEN
        assert test_bid == actual

    @mock.patch("yfinance.Ticker.info", new_callable=PropertyMock)
    def test_bid_price_regular_market(self, mock_ticker):
        """
        Test that regularMarketPrice is returned if bid price is 0
        """
        # GIVEN
        test_bid = 0
        regular_market_price = 42.22
        mock_ticker.return_value = {
            "bid": test_bid,
            "regularMarketPrice": regular_market_price,
        }
        holding = Holding.objects.all()[0]
        # WHEN
        actual = holding.bid_price()
        # THEN
        assert regular_market_price == actual

    @mock.patch("yfinance.Ticker.info", new_callable=PropertyMock)
    def test_bid_price_none(self, mock_ticker):
        """
        Test that if bid is not present in stock info, None is returned
        """
        # GIVEN
        mock_ticker.return_value = {}
        holding = Holding.objects.all()[0]
        # WHEN
        actual = holding.bid_price()
        # THEN
        assert actual is None

    @mock.patch("trade_simulation.models.Holding.bid_price", return_value=200)
    def market_value(self, mock_bid_price):
        """
        Test fetching market value succeeds
        """
        # GIVEN
        holding = Holding.objects.all()[0]
        expected = 600
        # WHEN
        actual = holding.market_value()
        # THEN
        assert expected == actual


class OptionTestCase(TestCase):
    def setUp(self):
        # Create game
        Game.objects.create(title="Test Game", rules="test rules")
        game = Game.objects.all()[0]
        # Create portfolio
        Portfolio.objects.create(title="Test portfolio", game=game)
        # Create option
        portfolio = Portfolio.objects.all()[0]
        Option.objects.create(portfolio=portfolio,
                              contract="AAPL211223C00148000",
                              quantity=2)
        Option.objects.create(portfolio=portfolio,
                              contract="TSLA211231P01115000",
                              quantity=1)

    def test_str(self):
        """
        Test __str__() returns contract
        """
        # GIVEN
        opt = Option.objects.get(contract="AAPL211223C00148000")
        # WHEN / THEN
        self.assertEqual(opt.__str__(), "AAPL211223C00148000")

    def test_ticker(self):
        """
        Test finding stock ticker from contract symbol
        """
        # GIVEN
        opt1 = Option.objects.get(contract="AAPL211223C00148000")
        opt2 = Option.objects.get(contract="TSLA211231P01115000")
        # WHEN
        ticker1 = opt1.ticker()
        ticker2 = opt2.ticker()
        # THEN
        self.assertEqual(ticker1, "AAPL")
        self.assertEqual(ticker2, "TSLA")

    def test_expiration_success(self):
        """
        Test finding contract expiration date from contract symbol
        """
        # GIVEN
        opt1 = Option.objects.get(contract="AAPL211223C00148000")
        opt2 = Option.objects.get(contract="TSLA211231P01115000")
        # WHEN
        date1 = opt1.expiration()
        date2 = opt2.expiration()
        # THEN
        self.assertEqual(date1, datetime(2021, 12, 23, 0, 0))
        self.assertEqual(date2, datetime(2021, 12, 31, 0, 0))

    def test_expiration_valueerror(self):
        """
        Test that a faulty string returns None for expiration date
        """
        # GIVEN
        portfolio = Portfolio.objects.get(title="Test portfolio")
        Option.objects.create(portfolio=portfolio,
                              contract="AAPL2X122BC00148000",
                              quantity=3)
        opt = Option.objects.get(contract="AAPL2X122BC00148000")
        # WHEN
        date = opt.expiration()
        # THEN
        self.assertIsNone(date)

    def test_option_type(self):
        """
        Test finding option type from contract symbol
        """
        # GIVEN
        opt1 = Option.objects.get(contract="AAPL211223C00148000")
        opt2 = Option.objects.get(contract="TSLA211231P01115000")
        # WHEN
        option_type1 = opt1.option_type()
        option_type2 = opt2.option_type()
        # THEN
        self.assertEqual(option_type1, 'C')
        self.assertEqual(option_type2, 'P')

    def test_strike_price(self):
        """
        Test finding strike price from contract symbol
        """
        # GIVEN
        opt1 = Option.objects.get(contract="AAPL211223C00148000")
        opt2 = Option.objects.get(contract="TSLA211231P01115000")
        # WHEN
        strike_price1 = opt1.strike_price()
        strike_price2 = opt2.strike_price()
        # THEN
        self.assertEqual(strike_price1, 148.0)
        self.assertEqual(strike_price2, 1115.0)

    def test_get_info_no_expdate(self):
        """
        Test that get_info returns None if expiration date is missing
        """
        # GIVEN
        portfolio = Portfolio.objects.get(title="Test portfolio")
        Option.objects.create(portfolio=portfolio,
                              contract="AAPL2X122BC00148000",
                              quantity=3)
        opt = Option.objects.get(contract="AAPL2X122BC00148000")
        # WHEN
        info = opt.get_info()
        # THEN
        self.assertIsNone(info)

    def test_get_info_bad_option_type(self):
        """
        Test that get_info returns None if option type is not 'C' or 'P'
        """
        # GIVEN
        portfolio = Portfolio.objects.get(title="Test portfolio")
        Option.objects.create(portfolio=portfolio,
                              contract="AAPL211223Q00148000",
                              quantity=3)
        opt = Option.objects.get(contract="AAPL211223Q00148000")
        # WHEN
        info = opt.get_info()
        # THEN
        self.assertIsNone(info)

    def test_get_info_bad_expiration_date(self):
        """
        Test that get_info returns None if expiration date is not available in yfinance
        """
        # GIVEN
        portfolio = Portfolio.objects.get(title="Test portfolio")
        Option.objects.create(portfolio=portfolio,
                              contract="AAPL201223C00148000",
                              quantity=3)
        opt = Option.objects.get(contract="AAPL201223C00148000")
        # WHEN
        info = opt.get_info()
        # THEN
        self.assertIsNone(info)

    @mock.patch("yfinance.Ticker.option_chain",
                return_value=SimpleNamespace(calls=DataFrame(columns=["contractSymbol"]),
                                             puts=DataFrame(columns=["contractSymbol"]))
                )
    def test_get_info_contract_not_in_list(self, mock_info):
        """
        Test get_info returns None if contract not in the list for valid query parameters
        """
        # GIVEN
        opt1 = Option.objects.get(contract="AAPL211223C00148000")
        opt2 = Option.objects.get(contract="TSLA211231P01115000")
        # WHEN
        info1 = opt1.get_info()
        info2 = opt2.get_info()
        # THEN
        self.assertIsNone(info1)
        self.assertIsNone(info2)

    @mock.patch("trade_simulation.models.Option.get_info", return_value={"ask": 15.40})
    def test_askprice_calloption_success(self, mock_info):
        """
        Test fetching ask price on call option succeeds
        """
        # GIVEN
        option = Option.objects.get(contract="AAPL211223C00148000")
        # WHEN
        actual = option.ask_price()
        # THEN
        self.assertAlmostEqual(actual, 1540.0)

    @mock.patch("trade_simulation.models.Option.get_info", return_value={"ask": 148.30})
    def test_askprice_putoption_success(self, mock_info):
        """
        Test fetching ask price on put option succeeds
        """
        # GIVEN
        option = Option.objects.get(contract="TSLA211231P01115000")
        # WHEN
        actual = option.ask_price()
        # THEN
        print(actual)
        self.assertAlmostEqual(actual, 14830.0)

    @mock.patch("trade_simulation.models.Option.get_info", return_value={"ask": 0, "lastPrice": 16.00})
    def test_askprice_calloption_lastprice(self, mock_info):
        """
        Test that lastPrice on call option is returned if ask price is 0
        """
        # GIVEN
        option = Option.objects.get(contract="AAPL211223C00148000")
        # WHEN
        actual = option.ask_price()
        # THEN
        self.assertAlmostEqual(actual, 1600.0)

    @mock.patch("trade_simulation.models.Option.get_info", return_value={"ask": 0, "lastPrice": 141.75})
    def test_askprice_putoption_lastprice(self, mock_info):
        """
        Test that lastPrice on put option is returned if ask price is 0
        """
        # GIVEN
        option = Option.objects.get(contract="TSLA211231P01115000")
        # WHEN
        actual = option.ask_price()
        # THEN
        self.assertAlmostEqual(actual, 14175.0)

    @mock.patch("trade_simulation.models.Option.get_info", return_value=None)
    def test_ask_price_none(self, mock_info):
        """
        Test that if option info not found, None is returned
        """
        # GIVEN
        option = Option.objects.get(contract="AAPL211223C00148000")
        # WHEN
        actual = option.ask_price()
        # THEN
        self.assertIsNone(actual)

    @mock.patch("trade_simulation.models.Option.get_info", return_value={"bid": 14.90})
    def test_bidprice_calloption_success(self, mock_info):
        """
        Test fetching bid price on call option succeeds
        """
        # GIVEN
        option = Option.objects.get(contract="AAPL211223C00148000")
        # WHEN
        actual = option.bid_price()
        # THEN
        self.assertAlmostEqual(actual, 1490.00)

    @mock.patch("trade_simulation.models.Option.get_info", return_value={"bid": 141.45})
    def test_bidprice_putoption_success(self, mock_info):
        """
        Test fetching bid price on put option succeeds
        """
        # GIVEN
        option = Option.objects.get(contract="TSLA211231P01115000")
        # WHEN
        actual = option.bid_price()
        # THEN
        print(actual)
        self.assertAlmostEqual(actual, 14145.00)

    @mock.patch("trade_simulation.models.Option.get_info", return_value={"bid": 0, "lastPrice": 16.00})
    def test_bidprice_calloption_lastprice(self, mock_info):
        """
        Test that lastPrice on call option is returned if bid price is 0
        """
        # GIVEN
        option = Option.objects.get(contract="AAPL211223C00148000")
        # WHEN
        actual = option.bid_price()
        # THEN
        self.assertAlmostEqual(actual, 1600.0)

    @mock.patch("trade_simulation.models.Option.get_info", return_value={"bid": 0, "lastPrice": 141.75})
    def test_bidprice_putoption_lastprice(self, mock_info):
        """
        Test that lastPrice on put option is returned if bid price is 0
        """
        # GIVEN
        option = Option.objects.get(contract="TSLA211231P01115000")
        # WHEN
        actual = option.bid_price()
        # THEN
        self.assertAlmostEqual(actual, 14175.0)

    @mock.patch("trade_simulation.models.Option.get_info", return_value=None)
    def test_bid_price_none(self, mock_info):
        """
        Test that if bid is not present in option info, None is returned
        """
        # GIVEN
        option = Option.objects.get(contract="AAPL211223C00148000")
        # WHEN
        actual = option.bid_price()
        # THEN
        self.assertIsNone(actual)


class TransactionTestCase(TestCase):
    def setUp(self):
        # Create transaction
        Transaction.objects.create(
            ticker="AAPL", trade_type="BUY", shares=1, bought_price=122.34
        )

    def test_str(self):
        """
        Test __str__() returns ticker
        """
        # GIVEN
        t = Transaction.objects.all()[0]
        # WHEN / THEN
        assert t.__str__() == "AAPL"
