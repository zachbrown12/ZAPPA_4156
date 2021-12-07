from django.test import TestCase, RequestFactory
import unittest.mock as mock
from trade_simulation.models import Game, Portfolio, Holding, Transaction
from django.contrib.auth.models import User
from api.helpers import (
    _get_game_standings_helper,
    _get_game_helper,
    _create_game_helper,
    _delete_game_helper,
    _get_portfolios_helper,
    _get_portfolio_helper,
    _delete_portfolio_helper,
    _post_portfolio_helper,
    _trade_stock_helper,
    _trade_option_helper,
    _get_holding_helper,
    _get_option_helper,
)
from api.views import (
    get_routes,
    handle_games,
    handle_game,
    handle_portfolios,
    handle_portfolio,
    trade,
    handle_holdings,
    handle_holding,
    handle_options,
    handle_option,
    handle_transactions,
    handle_transaction,
)
from .utils import find_game_by_title, find_portfolio, find_holding, find_option

TEST_GAME_TITLE = "Game Title"
TEST_RULES = "Test Rules"
TEST_PORTFOLIO_TITLE = "Portfolio Title"

GAME_URL = "/game/"
PORTFOLIO_URL = "/portfolio/"
TRADE_URL = "/portfolio/trade"
HOLDING_URL = "/holding/"
OPTION_URL = "/option/"
TRANSACTION_URL = "/transaction/"


class HelperTestCase(TestCase):

    def setUp(self):
        self.test_user = User.objects.create_user(username='test_user',
                                                  email='test@user.com',
                                                  password='12345')

    def _test_create_game_helper_success(self):
        """
        Test that we can successfully create a game
        """
        # GIVEN
        title = TEST_GAME_TITLE
        # WHEN
        _create_game_helper(title, TEST_RULES, 10000)
        games = Game.objects.all()
        # THEN
        assert len(games) == 1
        game = games[0]
        assert game.title == title

    def _test_create_game_helper_duplicate_title(self):
        """
        Test that creating a game fails when we create a game with same title as existing game
        """
        # GIVEN
        title = TEST_GAME_TITLE
        # WHEN
        _create_game_helper(title, TEST_RULES, 10000)
        games = Game.objects.all()
        # THEN
        assert len(games) == 1
        game = games[0]
        assert game.title == title
        # WHEN / THEN
        with self.assertRaises(Exception):
            _create_game_helper(title, TEST_RULES, 1000)

    @mock.patch(
        "trade_simulation.models.Game.objects.create", return_value=RuntimeError
    )
    def _test_create_game_helper_runtime_error(self, mock_create):
        # GIVEN
        title = TEST_GAME_TITLE
        # WHEN / THEN
        with self.assertRaises(Exception):
            _create_game_helper(title, TEST_RULES, 10000)

    def test_get_game_standings_helper(self):
        """
        Test that we can successfully get game standings
        """
        # GIVEN
        for i in range(3):
            title = f"{TEST_GAME_TITLE} {i}"
            _create_game_helper(title, TEST_RULES, 10000)
        # WHEN
        actual = _get_game_standings_helper()
        # THEN
        assert len(actual) == 3

    def test_get_game_standings_helper_no_games(self):
        """
        Test that helper returns None when no games
        """
        # GIVEN
        expected = None
        # WHEN
        actual = _get_game_standings_helper()
        # THEN
        assert expected == actual

    def test_delete_game_helper_success(self):
        """
        Test that we can delete an existing game successfully
        """
        # GIVEN
        title = TEST_GAME_TITLE
        _create_game_helper(title, TEST_RULES, 10000)

        # WHEN
        _delete_game_helper(title)

        # THEN
        games = Game.objects.all()
        assert len(games) == 0
        assert find_game_by_title(title) is None

    def test_delete_game_helper_not_exist(self):
        """
        Test that exception is thrown if try to delete a game that does not exist
        """
        # GIVEN
        title = TEST_GAME_TITLE
        # WHEN / THEN
        with self.assertRaises(Exception):
            _delete_game_helper(title)

    def test_get_game_helper_success(self):
        """
        Test that we can get a game successfully
        """
        title = TEST_GAME_TITLE
        _create_game_helper(title, TEST_RULES, 10000)
        # WHEN
        game = _get_game_helper(title)
        # THEN
        assert game["title"] == title

    def test_get_game_helper_not_exist(self):
        """
        Test that we throw an exception if game does not exist
        """
        # GIVEN
        title = TEST_GAME_TITLE
        # WHEN / THEN
        with self.assertRaises(Exception):
            _get_game_helper(title)

    def test_get_portfolio_helper_success(self):
        """
        Test that we can fetch portfolio by title and game successfully
        """
        # GIVEN
        game_title = TEST_GAME_TITLE
        portfolio_title = TEST_PORTFOLIO_TITLE
        _create_game_helper(game_title, TEST_RULES, 10000)
        _post_portfolio_helper(portfolio_title, game_title, self.test_user.username)

        # WHEN
        portfolio = _get_portfolio_helper(portfolio_title, game_title)

        # THEN
        assert portfolio["title"] == portfolio_title

    def test_get_portfolio_helper_not_found(self):
        """
        Test that exception raised if portfolio not found
        """
        # GIVEN
        game_title = TEST_GAME_TITLE
        portfolio_title = TEST_PORTFOLIO_TITLE
        _create_game_helper(game_title, TEST_RULES, 10000)

        # WHEN / THEN
        with self.assertRaises(Exception):
            _get_portfolio_helper(portfolio_title, game_title)

    def test_get_portfolios_success(self):
        """
        Test that we can fetch all portfolios successfully
        """
        # GIVEN
        game_title = TEST_GAME_TITLE
        _create_game_helper(game_title, TEST_RULES, 10000)
        for i in range(3):
            portfolio_title = f"{TEST_PORTFOLIO_TITLE} {i}"
            _post_portfolio_helper(portfolio_title, game_title, self.test_user.username)
        # WHEN
        portfolios = _get_portfolios_helper()
        # THEN
        assert len(portfolios) == 3

    @mock.patch(
        "trade_simulation.models.Portfolio.objects.all", return_value=RuntimeError
    )
    def test_get_portfolios_error(self, mock_portfolio):
        """
        Test that when runtime error occurs when getting portfolios, exception is thrown
        """
        # GIVEN
        game_title = TEST_GAME_TITLE
        _create_game_helper(game_title, TEST_RULES, 10000)
        # WHEN / THEN
        with self.assertRaises(Exception):
            _get_portfolios_helper()

    def test_delete_portfolio_success(self):
        """
        Test that we can delete an existing portfolio successfully
        """
        # GIVEN
        game_title = TEST_GAME_TITLE
        portfolio_title = TEST_PORTFOLIO_TITLE
        _create_game_helper(game_title, TEST_RULES, 10000)
        _post_portfolio_helper(portfolio_title, game_title, self.test_user.username)
        # WHEN
        _delete_portfolio_helper(portfolio_title, game_title)
        # THEN
        p = find_portfolio(portfolio_title, game_title)
        assert p is None

    def test_delete_portfolio_not_exist(self):
        """
        Test that deleting a portfolio that does not exist throws an exception
        """
        # GIVEN
        game_title = TEST_GAME_TITLE
        portfolio_title = TEST_PORTFOLIO_TITLE
        _create_game_helper(game_title, TEST_RULES, 10000)
        # WHEN / THEN
        with self.assertRaises(Exception):
            _delete_portfolio_helper(portfolio_title, game_title)

    def test_create_portfolio_game_not_exist(self):
        """
        Test that creating a portfolio in a game that does not exist throws an exception
        """
        # GIVEN
        game_title = TEST_GAME_TITLE
        portfolio_title = TEST_PORTFOLIO_TITLE
        # WHEN / THEN
        with self.assertRaises(Exception):
            _post_portfolio_helper(portfolio_title, game_title, self.test_user.username)

    def test_create_portfolio_already_exists(self):
        """
        Test that creating a portfolio in a game that already has a portfolio of that name throws an exception
        """
        # GIVEN
        game_title = TEST_GAME_TITLE
        portfolio_title = TEST_PORTFOLIO_TITLE
        _create_game_helper(game_title, TEST_RULES, 10000)
        _post_portfolio_helper(portfolio_title, game_title, self.test_user.username)
        # WHEN / THEN
        with self.assertRaises(Exception):
            _post_portfolio_helper(portfolio_title, game_title, self.test_user.username)

    def test_create_portfolio_no_username(self):
        """
        Test that creating a portfolio in a game without specifying a username throws an exception
        """
        # GIVEN
        game_title = TEST_GAME_TITLE
        portfolio_title = TEST_PORTFOLIO_TITLE
        _create_game_helper(game_title, TEST_RULES, 10000)
        # WHEN / THEN
        with self.assertRaises(Exception):
            _post_portfolio_helper(portfolio_title, game_title, None)

    def test_create_portfolio_username_not_found(self):
        """
        Test that creating a portfolio in a game with a bad username throws an exception
        """
        # GIVEN
        game_title = TEST_GAME_TITLE
        portfolio_title = TEST_PORTFOLIO_TITLE
        _create_game_helper(game_title, TEST_RULES, 10000)
        # WHEN / THEN
        with self.assertRaises(Exception):
            _post_portfolio_helper(portfolio_title, game_title, "ldsakfkwdsj")

    @mock.patch("trade_simulation.models.Holding.ask_price", return_value=200)
    def test_trade_stock_helper_success_buy(self, mock_buy_stock):
        """
        Test that we buy a stock successfully if shares > 0
        """
        # GIVEN
        game_title = TEST_GAME_TITLE
        portfolio_title = TEST_PORTFOLIO_TITLE
        _create_game_helper(game_title, TEST_RULES, 10000)
        _post_portfolio_helper(portfolio_title, game_title, self.test_user.username)
        ticker = "AAPL"
        shares = 3
        # WHEN
        _trade_stock_helper(portfolio_title, game_title, ticker, shares)
        # THEN
        holding = find_holding(portfolio_title, game_title, ticker)
        assert holding.shares == shares

    @mock.patch("trade_simulation.models.Option.ask_price", return_value=2000)
    @mock.patch("trade_simulation.models.Holding.ask_price", return_value=200)
    def test_trade_stock_helper_option_success_buy(self, mock_buy_stock, mock_buy_option):
        """
        Test that we buy a stock while exercising option successfully if shares > 0
        """
        # GIVEN
        game_title = TEST_GAME_TITLE
        portfolio_title = TEST_PORTFOLIO_TITLE
        _create_game_helper(game_title, TEST_RULES, 10000)
        _post_portfolio_helper(portfolio_title, game_title, self.test_user.username)
        ticker = "AAPL"
        shares = 3
        contract = "AAPL211223C00148000"
        quantity = 1
        # WHEN
        _trade_option_helper(portfolio_title, game_title, contract, quantity)
        _trade_stock_helper(portfolio_title, game_title, ticker, shares, exercise=contract)
        # THEN
        holding = find_holding(portfolio_title, game_title, ticker)
        assert holding.shares == shares

    @mock.patch("trade_simulation.models.Holding.bid_price", return_value=200)
    def test_trade_stock_helper_success_sell(self, mock_sell_stock):
        """
        Test that we sell a stock successfully if shares < 0
        """
        # GIVEN
        game_title = TEST_GAME_TITLE
        portfolio_title = TEST_PORTFOLIO_TITLE
        _create_game_helper(game_title, TEST_RULES, 10000)
        _post_portfolio_helper(portfolio_title, game_title, self.test_user.username)
        ticker = "AAPL"
        shares = 3
        _trade_stock_helper(portfolio_title, game_title, ticker, shares + 1)
        # WHEN
        _trade_stock_helper(portfolio_title, game_title, ticker, -shares)
        # THEN
        holding = find_holding(portfolio_title, game_title, ticker)
        assert holding.shares == 1

    @mock.patch("trade_simulation.models.Option.ask_price", return_value=9000)
    @mock.patch("trade_simulation.models.Holding.bid_price", return_value=200)
    def test_trade_stock_helper_option_success_sell(self, mock_sell_stock, mock_buy_option):
        """
        Test that we sell a stock while exercising option successfully if shares < 0
        """
        # GIVEN
        game_title = TEST_GAME_TITLE
        portfolio_title = TEST_PORTFOLIO_TITLE
        _create_game_helper(game_title, TEST_RULES, 30000)
        _post_portfolio_helper(portfolio_title, game_title, self.test_user.username)
        ticker = "TSLA"
        shares = 2
        contract = "TSLA211231P01115000"
        quantity = 1
        _trade_stock_helper(portfolio_title, game_title, ticker, shares + 1)
        _trade_option_helper(portfolio_title, game_title, contract, quantity)
        # WHEN
        _trade_stock_helper(portfolio_title, game_title, ticker, -shares, exercise=contract)
        # THEN
        holding = find_holding(portfolio_title, game_title, ticker)
        assert holding.shares == 1

    def test_trade_stock_helper_error(self):
        """
        Test that we cannot buy or sell a stock if portfolio does not exist
        """
        # GIVEN
        game_title = TEST_GAME_TITLE
        portfolio_title = TEST_PORTFOLIO_TITLE
        _create_game_helper(game_title, TEST_RULES, 10000)
        # WHEN / THEN
        with self.assertRaises(Exception):
            _trade_stock_helper(portfolio_title, game_title, "AAPL", 3)

    @mock.patch("api.helpers._trade_option_helper", return_value=None)
    def test_trade_option_helper_success_buy(self, mock_buy_option):
        """
        Test that we buy an option successfully if quantity > 0
        """
        # GIVEN
        game_title = TEST_GAME_TITLE
        portfolio_title = TEST_PORTFOLIO_TITLE
        _create_game_helper(game_title, TEST_RULES, 10000)
        _post_portfolio_helper(portfolio_title, game_title, self.test_user.username)
        contract = "AAPL211223C00148000"
        quantity = 1.0
        # WHEN
        _trade_option_helper(portfolio_title, game_title, contract, quantity)
        # THEN
        option = find_option(portfolio_title, game_title, contract)
        assert option.quantity == quantity

    @mock.patch("api.helpers._trade_option_helper")
    def test_trade_option_helper_success_sell(self, mock_sell_option):
        """
        Test that we sell an option successfully if quantity < 0
        """
        # GIVEN
        game_title = TEST_GAME_TITLE
        portfolio_title = TEST_PORTFOLIO_TITLE
        _create_game_helper(game_title, TEST_RULES, 10000)
        _post_portfolio_helper(portfolio_title, game_title, self.test_user.username)
        contract = "AAPL211223C00148000"
        quantity = 1.0
        _trade_option_helper(portfolio_title, game_title, contract, quantity + 1)
        # WHEN
        _trade_option_helper(portfolio_title, game_title, contract, -quantity)
        # THEN
        option = find_option(portfolio_title, game_title, contract)
        assert option.quantity == 1

    def test_trade_option_helper_error(self):
        """
        Test that we cannot buy or sell an option if portfolio does not exist
        """
        # GIVEN
        game_title = TEST_GAME_TITLE
        portfolio_title = TEST_PORTFOLIO_TITLE
        _create_game_helper(game_title, TEST_RULES, 10000)
        # WHEN / THEN
        with self.assertRaises(Exception):
            _trade_option_helper(portfolio_title, game_title, "AAPL211223C00148000", 1.0)

    def test_get_holding_helper_success(self):
        """
        Test that we can successfully get a holding for a portfolio
        """
        # GIVEN
        game_title = TEST_GAME_TITLE
        portfolio_title = TEST_PORTFOLIO_TITLE
        _create_game_helper(game_title, TEST_RULES, 10000)
        _post_portfolio_helper(portfolio_title, game_title, self.test_user.username)
        ticker = "AAPL"
        shares = 3
        _trade_stock_helper(portfolio_title, game_title, ticker, shares)
        # WHEN
        data = _get_holding_helper(portfolio_title, game_title, ticker)
        # THEN
        assert data["ticker"] == ticker

    def test_get_holding_helper_error_not_exist(self):
        """
        Test that throws an error if portfolio does not exist
        """
        # GIVEN
        game_title = TEST_GAME_TITLE
        portfolio_title = TEST_PORTFOLIO_TITLE
        _create_game_helper(game_title, TEST_RULES, 10000)
        # WHEN / THEN
        with self.assertRaises(Exception):
            _get_holding_helper(portfolio_title, game_title, "AAPL")

    def test_get_option_helper_success(self):
        """
        Test that we can successfully get an option in a portfolio
        """
        # GIVEN
        game_title = TEST_GAME_TITLE
        portfolio_title = TEST_PORTFOLIO_TITLE
        _create_game_helper(game_title, TEST_RULES, 10000)
        _post_portfolio_helper(portfolio_title, game_title, self.test_user.username)
        contract = "AAPL211223C00148000"
        quantity = 1.0
        _trade_option_helper(portfolio_title, game_title, contract, quantity)
        # WHEN
        data = _get_option_helper(portfolio_title, game_title, contract)
        # THEN
        assert data["contract"] == contract

    def test_get_option_helper_error_not_exist(self):
        """
        Test that throws an error if portfolio does not exist
        """
        # GIVEN
        game_title = TEST_GAME_TITLE
        portfolio_title = TEST_PORTFOLIO_TITLE
        _create_game_helper(game_title, TEST_RULES, 10000)
        # WHEN / THEN
        with self.assertRaises(Exception):
            _get_option_helper(portfolio_title, game_title, "AAPL211223C00148000")


class ViewTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.test_user = User.objects.create_user(username='test_user',
                                                  email='test@user.com',
                                                  password='12345')

    def test_routes(self):
        """
        Test that we can get the routes listing
        """
        # GIVEN
        request = self.factory.get('')
        # WHEN/THEN
        self.assertEqual(get_routes(request).status_code, 200)

    def test_handle_games_success(self):
        """
        Test that we can get a game successfully
        """
        # GIVEN
        request = self.factory.get('/games/')
        game_title = TEST_GAME_TITLE
        _create_game_helper(game_title, TEST_RULES, 10000)
        # WHEN / THEN
        self.assertEqual(handle_games(request).status_code, 200)

    def test_handle_game_get(self):
        """
        Test that we can get a game successfully
        """
        # GIVEN
        request = self.factory.get(GAME_URL)
        game_title = TEST_GAME_TITLE
        _create_game_helper(game_title, TEST_RULES, 10000)
        # WHEN / THEN
        self.assertEqual(handle_game(request, game_title).status_code, 200)

    def test_handle_game_get_fail(self):
        """
        Tests failure on getting a game when it does not exist.
        """
        # GIVEN
        request = self.factory.get(GAME_URL)
        game_title = TEST_GAME_TITLE
        _create_game_helper(game_title, TEST_RULES, 10000)
        # WHEN / THEN
        self.assertEqual(handle_game(request, "BlahBlah").status_code, 500)

    def test_handle_game_post(self):
        """
        Tests that we can create a game successfully
        """
        # GIVEN
        request = self.factory.post(GAME_URL)
        game_title = TEST_GAME_TITLE
        # WHEN / THEN
        self.assertEqual(handle_game(request, game_title).status_code, 200)

    def test_handle_game_post_fail(self):
        """
        Tests failure on creating games
        """
        # GIVEN
        data = {'rules': 'kill or be killed', 'startingBalance': 15000}
        request = self.factory.post(GAME_URL, data)
        game_title = TEST_GAME_TITLE
        _create_game_helper(game_title, TEST_RULES, 10000)
        # WHEN / THEN
        self.assertEqual(handle_game(request, game_title).status_code, 500)

    def test_handle_game_delete(self):
        """
        Tests we can delete a game successfully
        """
        # GIVEN
        request = self.factory.delete(GAME_URL)
        game_title = TEST_GAME_TITLE
        _create_game_helper(game_title, TEST_RULES, 10000)
        # WHEN / THEN
        self.assertEqual(handle_game(request, game_title).status_code, 200)

    def test_handle_game_delete_fail(self):
        """
        Tests failure on deleting games
        """
        # GIVEN
        request = self.factory.delete(GAME_URL)
        game_title = TEST_GAME_TITLE
        _create_game_helper(game_title, TEST_RULES, 10000)
        # WHEN / THEN
        self.assertEqual(handle_game(request, "BlahBlah").status_code, 500)

    def test_handle_portfolios_success(self):
        """
        Test that we can get all portfolios successfully
        """
        # GIVEN
        request = self.factory.get('/portfolios/')
        game_title = TEST_GAME_TITLE
        portfolio_title = TEST_PORTFOLIO_TITLE
        _create_game_helper(game_title, TEST_RULES, 10000)
        _post_portfolio_helper(portfolio_title, game_title, self.test_user.username)
        # WHEN / THEN
        self.assertEqual(handle_portfolios(request).status_code, 200)

    def test_handle_portfolio_get(self):
        """
        Test that we can get a portfolio successfully
        """
        # GIVEN
        request = self.factory.get(PORTFOLIO_URL)
        game_title = TEST_GAME_TITLE
        portfolio_title = TEST_PORTFOLIO_TITLE
        _create_game_helper(game_title, TEST_RULES, 10000)
        _post_portfolio_helper(portfolio_title, game_title, self.test_user.username)
        # WHEN / THEN
        self.assertEqual(handle_portfolio(request, TEST_GAME_TITLE, TEST_PORTFOLIO_TITLE).status_code, 200)

    def test_handle_portfolio_get_fail(self):
        """
        Tests failure on getting a portfolio when it does not exist.
        """
        # GIVEN
        request = self.factory.get(PORTFOLIO_URL)
        game_title = TEST_GAME_TITLE
        portfolio_title = TEST_PORTFOLIO_TITLE
        _create_game_helper(game_title, TEST_RULES, 10000)
        _post_portfolio_helper(portfolio_title, game_title, self.test_user.username)
        # WHEN / THEN
        self.assertEqual(handle_portfolio(request, "BlahBlah", "BlahBlah").status_code, 500)

    def test_handle_portfolio_post(self):
        """
        Tests that we can create a portfolio successfully
        """
        # GIVEN
        data = {"username": self.test_user.username}
        request = self.factory.post(PORTFOLIO_URL, data)
        game_title = TEST_GAME_TITLE
        portfolio_title = TEST_PORTFOLIO_TITLE
        _create_game_helper(game_title, TEST_RULES, 10000)
        # WHEN / THEN
        self.assertEqual(handle_portfolio(request, game_title, portfolio_title).status_code, 200)

    def test_handle_portfolio_post_already_exists(self):
        """
        Tests failure on creating portfolio if one of the same name already exists in game
        """
        # GIVEN
        data = {"username": self.test_user.username}
        request = self.factory.post(PORTFOLIO_URL, data)
        game_title = TEST_GAME_TITLE
        portfolio_title = TEST_PORTFOLIO_TITLE
        _create_game_helper(game_title, TEST_RULES, 10000)
        _post_portfolio_helper(portfolio_title, game_title, self.test_user.username)
        # WHEN / THEN
        self.assertEqual(handle_portfolio(request, game_title, portfolio_title).status_code, 500)

    def test_handle_portfolio_post_missing_username(self):
        """
        Tests failure on creating portfolio if username is missing from the request
        """
        # GIVEN
        request = self.factory.post(PORTFOLIO_URL)
        game_title = TEST_GAME_TITLE
        portfolio_title = TEST_PORTFOLIO_TITLE
        _create_game_helper(game_title, TEST_RULES, 10000)
        # WHEN / THEN
        self.assertEqual(handle_portfolio(request, game_title, portfolio_title).status_code, 500)

    def test_handle_portfolio_delete(self):
        """
        Tests we can delete a portfolio successfully
        """
        # GIVEN
        request = self.factory.delete(PORTFOLIO_URL)
        game_title = TEST_GAME_TITLE
        portfolio_title = TEST_PORTFOLIO_TITLE
        _create_game_helper(game_title, TEST_RULES, 10000)
        _post_portfolio_helper(portfolio_title, game_title, self.test_user.username)
        # WHEN / THEN
        self.assertEqual(handle_portfolio(request, game_title, portfolio_title).status_code, 200)

    def test_handle_portfolio_delete_fail(self):
        """
        Tests failure on deleting portfolios
        """
        # GIVEN
        request = self.factory.delete(PORTFOLIO_URL)
        game_title = TEST_GAME_TITLE
        portfolio_title = TEST_PORTFOLIO_TITLE
        _create_game_helper(game_title, TEST_RULES, 10000)
        _post_portfolio_helper(portfolio_title, game_title, self.test_user.username)
        # WHEN / THEN
        self.assertEqual(handle_portfolio(request, "BlahBlah", "BlahBlah").status_code, 500)

    @mock.patch("api.helpers._trade_stock_helper", return_value=None)
    def test_trade_buy_stock(self, mock_trade):
        """
        Tests we can buy a stock successfully
        """
        # GIVEN
        game_title = TEST_GAME_TITLE
        portfolio_title = TEST_PORTFOLIO_TITLE
        data = {"portfolioTitle": portfolio_title,
                "gameTitle": game_title,
                "securityType": "stock",
                "ticker": "AAPL",
                "shares": 4.0,
                }
        request = self.factory.post(TRADE_URL, data)
        _create_game_helper(game_title, TEST_RULES, 10000)
        _post_portfolio_helper(portfolio_title, game_title, self.test_user.username)
        # WHEN / THEN
        self.assertEqual(trade(request).status_code, 200)

    @mock.patch("api.helpers._trade_stock_helper", return_value=None)
    def test_trade_buy_stock_bad_ticker(self, mock_trade):
        """
        Tests that a buying a stock with invalid ticker raises an error
        """
        # GIVEN
        game_title = TEST_GAME_TITLE
        portfolio_title = TEST_PORTFOLIO_TITLE
        data = {"portfolioTitle": portfolio_title,
                "gameTitle": game_title,
                "securityType": "stock",
                "ticker": "AAPX",
                "shares": 4.0,
                }
        request = self.factory.post(TRADE_URL, data)
        _create_game_helper(game_title, TEST_RULES, 10000)
        _post_portfolio_helper(portfolio_title, game_title, self.test_user.username)
        # WHEN / THEN
        self.assertEqual(trade(request).status_code, 500)

    @mock.patch("api.helpers._trade_option_helper", return_value=None)
    def test_trade_buy_call_option(self, mock_trade):
        """
        Tests we can buy a call option successfully
        """
        # GIVEN
        game_title = TEST_GAME_TITLE
        portfolio_title = TEST_PORTFOLIO_TITLE
        data = {"portfolioTitle": portfolio_title,
                "gameTitle": game_title,
                "securityType": "option",
                "contract": "AAPL211223C00148000",
                "quantity": 1.0
                }
        request = self.factory.post(TRADE_URL, data)
        _create_game_helper(game_title, TEST_RULES, 10000)
        _post_portfolio_helper(portfolio_title, game_title, self.test_user.username)
        # WHEN / THEN
        self.assertEqual(trade(request).status_code, 200)

    @mock.patch("api.helpers._trade_option_helper", return_value=None)
    def test_trade_buy_call_option_bad_contractname(self, mock_trade):
        """
        Tests that buying an option with a bad contract name raises an error
        """
        # GIVEN
        game_title = TEST_GAME_TITLE
        portfolio_title = TEST_PORTFOLIO_TITLE
        data = {"portfolioTitle": portfolio_title,
                "gameTitle": game_title,
                "securityType": "option",
                "contract": "AAPL211223X00148000",
                "quantity": 1.0
                }
        request = self.factory.post(TRADE_URL, data)
        _create_game_helper(game_title, TEST_RULES, 10000)
        _post_portfolio_helper(portfolio_title, game_title, self.test_user.username)
        # WHEN / THEN
        self.assertEqual(trade(request).status_code, 500)

    @mock.patch("api.helpers._trade_stock_helper", return_value=None)
    def test_trade_buy_stock_exercise(self, mock_trade):
        """
        Tests we can buy a stock while exercising a call option successfully
        """
        # GIVEN
        game_title = TEST_GAME_TITLE
        portfolio_title = TEST_PORTFOLIO_TITLE
        contract = "AAPL211223C00148000"
        data = {"portfolioTitle": portfolio_title,
                "gameTitle": game_title,
                "securityType": "stock",
                "ticker": "AAPL",
                "shares": 4.0,
                "exercise": contract,
                }
        request = self.factory.post(TRADE_URL, data)
        _create_game_helper(game_title, TEST_RULES, 10000)
        _post_portfolio_helper(portfolio_title, game_title, self.test_user.username)
        _trade_option_helper(portfolio_title, game_title, contract, 1.0)
        # WHEN / THEN
        self.assertEqual(trade(request).status_code, 200)

    def test_trade_bad_security_type(self):
        """
        Tests trade failure on bad security type
        """
        # GIVEN
        data = {'securityType': 'Blah'}
        request = self.factory.post(TRADE_URL, data)
        game_title = TEST_GAME_TITLE
        portfolio_title = TEST_PORTFOLIO_TITLE
        _create_game_helper(game_title, TEST_RULES, 10000)
        _post_portfolio_helper(portfolio_title, game_title, self.test_user.username)
        # WHEN / THEN
        self.assertEqual(trade(request).status_code, 500)

    def test_handle_holdings_success(self):
        """
        Test that we can get all holdings successfully
        """
        # GIVEN
        request = self.factory.get('/holdings/')
        game_title = TEST_GAME_TITLE
        portfolio_title = TEST_PORTFOLIO_TITLE
        _create_game_helper(game_title, TEST_RULES, 10000)
        _post_portfolio_helper(portfolio_title, game_title, self.test_user.username)
        ticker = "AAPL"
        shares = 3
        _trade_stock_helper(portfolio_title, game_title, ticker, shares)
        # WHEN / THEN
        self.assertEqual(handle_holdings(request).status_code, 200)

    def test_handle_holding_success(self):
        """
        Test that we can get a holding successfully
        """
        # GIVEN
        request = self.factory.get(HOLDING_URL)
        game_title = TEST_GAME_TITLE
        portfolio_title = TEST_PORTFOLIO_TITLE
        _create_game_helper(game_title, TEST_RULES, 10000)
        _post_portfolio_helper(portfolio_title, game_title, self.test_user.username)
        ticker = "AAPL"
        shares = 3
        _trade_stock_helper(portfolio_title, game_title, ticker, shares)
        # WHEN / THEN
        self.assertEqual(handle_holding(request, game_title, portfolio_title, ticker).status_code, 200)

    def test_handle_holding_not_found(self):
        """
        Test that a holding not found raises an exception
        """
        # GIVEN
        request = self.factory.get(HOLDING_URL)
        game_title = TEST_GAME_TITLE
        portfolio_title = TEST_PORTFOLIO_TITLE
        _create_game_helper(game_title, TEST_RULES, 10000)
        _post_portfolio_helper(portfolio_title, game_title, self.test_user.username)
        ticker = "AAPL"
        # WHEN / THEN
        self.assertEqual(handle_holding(request, game_title, portfolio_title, ticker).status_code, 500)

    def test_handle_options_success(self):
        """
        Test that we can get all options successfully
        """
        # GIVEN
        request = self.factory.get('/options/')
        game_title = TEST_GAME_TITLE
        portfolio_title = TEST_PORTFOLIO_TITLE
        _create_game_helper(game_title, TEST_RULES, 10000)
        _post_portfolio_helper(portfolio_title, game_title, self.test_user.username)
        contract = "AAPL211223C00148000"
        quantity = 4.0
        _trade_option_helper(portfolio_title, game_title, contract, quantity)
        # WHEN / THEN
        self.assertEqual(handle_options(request).status_code, 200)

    def test_handle_option_success(self):
        """
        Test that we can get an option successfully
        """
        # GIVEN
        request = self.factory.get(OPTION_URL)
        game_title = TEST_GAME_TITLE
        portfolio_title = TEST_PORTFOLIO_TITLE
        _create_game_helper(game_title, TEST_RULES, 10000)
        _post_portfolio_helper(portfolio_title, game_title, self.test_user.username)
        contract = "AAPL211223C00148000"
        quantity = 4.0
        _trade_option_helper(portfolio_title, game_title, contract, quantity)
        # WHEN / THEN
        self.assertEqual(handle_option(request, game_title, portfolio_title, contract).status_code, 200)

    def test_handle_option_not_found(self):
        """
        Test that an option not found raises an exception
        """
        # GIVEN
        request = self.factory.get(OPTION_URL)
        game_title = TEST_GAME_TITLE
        portfolio_title = TEST_PORTFOLIO_TITLE
        _create_game_helper(game_title, TEST_RULES, 10000)
        _post_portfolio_helper(portfolio_title, game_title, self.test_user.username)
        contract = "AAPL211223C00148000"
        # WHEN / THEN
        self.assertEqual(handle_option(request, game_title, portfolio_title, contract).status_code, 500)

    def test_handle_transactions_success(self):
        """
        Test that we can get all transactions successfully
        """
        # GIVEN
        request = self.factory.get('/transactions/')
        game_title = TEST_GAME_TITLE
        portfolio_title = TEST_PORTFOLIO_TITLE
        _create_game_helper(game_title, TEST_RULES, 10000)
        _post_portfolio_helper(portfolio_title, game_title, self.test_user.username)
        ticker = "AAPL"
        shares = 3
        _trade_stock_helper(portfolio_title, game_title, ticker, shares)
        # WHEN / THEN
        self.assertEqual(handle_transactions(request).status_code, 200)

    def test_handle_transaction_success(self):
        """
        Test that we can get one transaction successfully
        """
        # GIVEN
        request = self.factory.get(TRANSACTION_URL)
        game_title = TEST_GAME_TITLE
        portfolio_title = TEST_PORTFOLIO_TITLE
        _create_game_helper(game_title, TEST_RULES, 10000)
        _post_portfolio_helper(portfolio_title, game_title, self.test_user.username)
        ticker = "AAPL"
        shares = 3
        _trade_stock_helper(portfolio_title, game_title, ticker, shares)
        t = Transaction.objects.get(ticker=ticker)
        # WHEN / THEN
        self.assertEqual(handle_transaction(request, t.uid).status_code, 200)

    def test_handle_transaction_not_found(self):
        """
        Test that a transaction not found raises an exception
        """
        # GIVEN
        request = self.factory.get(TRANSACTION_URL)
        game_title = TEST_GAME_TITLE
        portfolio_title = TEST_PORTFOLIO_TITLE
        _create_game_helper(game_title, TEST_RULES, 10000)
        _post_portfolio_helper(portfolio_title, game_title, self.test_user.username)
        ticker = "AAPL"
        shares = 3
        _trade_stock_helper(portfolio_title, game_title, ticker, shares)
        # WHEN / THEN
        self.assertEqual(handle_transaction(request, "c971b071-7d59-4d96-be9b-710a463xxxxx").status_code, 500)
