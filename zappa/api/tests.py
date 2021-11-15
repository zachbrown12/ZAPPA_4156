from django.test import TestCase
import mock
from trade_simulation.models import Game, Portfolio, Holding, Transaction
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
    _buy_stock_helper,
    _sell_stock_helper,
    _get_holding_helper,
)
from .utils import find_game_by_title, find_portfolio


class HelperTestCase(TestCase):
    def _test_create_game_helper_success(self):
        """
        Test that we can successfully create a game
        """
        # GIVEN
        title = "Test Game"
        # WHEN
        _create_game_helper(title, "test rules", 10000)
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
        title = "Test Game"
        # WHEN
        _create_game_helper(title, "test rules", 10000)
        games = Game.objects.all()
        # THEN
        assert len(games) == 1
        game = games[0]
        assert game.title == title
        # WHEN / THEN
        with self.assertRaises(Exception):
            _create_game_helper(title, "test rules", 1000)

    @mock.patch(
        "trade_simulation.models.Game.objects.create", return_value=RuntimeError
    )
    def _test_create_game_helper_runtime_error(self, mock_create):
        # GIVEN
        title = "Test Game"
        # WHEN / THEN
        with self.assertRaises(Exception):
            _create_game_helper(title, "test rules", 10000)

    def test_get_game_standings_helper(self):
        """
        Test that we can successfully get game standings
        """
        # GIVEN
        for i in range(3):
            title = f"Test Game {i}"
            _create_game_helper(title, "test rules", 10000)
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
        title = "Test Game"
        _create_game_helper(title, "test rules", 10000)

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
        title = "Game Title"
        # WHEN / THEN
        with self.assertRaises(Exception):
            _delete_game_helper(title)

    def test_get_game_helper_success(self):
        """
        Test that we can get a game successfully
        """
        title = "Game title"
        _create_game_helper(title, "test rules", 10000)
        # WHEN
        game = _get_game_helper(title)
        # THEN
        assert game["title"] == title

    def test_get_game_helper_not_exist(self):
        """
        Test that we throw an exception if game does not exist
        """
        # GIVEN
        title = "Game title"
        # WHEN / THEN
        with self.assertRaises(Exception):
            _get_game_helper(title)

    def test_get_portfolio_helper_success(self):
        """
        Test that we can fetch portfolio by title and game successfully
        """
        # GIVEN
        game_title = "Game Title"
        portfolio_title = "Portfolio Title"
        _create_game_helper(game_title, "test rules", 10000)
        _post_portfolio_helper(portfolio_title, game_title)

        # WHEN
        portfolio = _get_portfolio_helper(portfolio_title, game_title)

        # THEN
        portfolio["title"] == portfolio_title

    def test_get_portfolio_helper_not_found(self):
        """
        Test that exception raised if portfolio not found
        """
        # GIVEN
        game_title = "Game Title"
        portfolio_title = "Portfolio Title"
        _create_game_helper(game_title, "test rules", 10000)

        # WHEN / THEN
        with self.assertRaises(Exception):
            _get_portfolio_helper(portfolio_title, game_title)

    def test_get_portfolios_success(self):
        """
        Test that we can fetch all portfolios successfully
        """
        # GIVEN
        game_title = "Test Game"
        _create_game_helper(game_title, "test rules", 10000)
        for i in range(3):
            portfolio_title = f"Portfolio Title {i}"
            _post_portfolio_helper(portfolio_title, game_title)
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
        game_title = "Test Game"
        _create_game_helper(game_title, "test rules", 10000)
        # WHEN / THEN
        with self.assertRaises(Exception):
            _get_portfolios_helper()

    def test_delete_portfolio_success(self):
        """
        Test that we can delete an existing portfolio successfully
        """
        # GIVEN
        game_title = "Game Title"
        portfolio_title = "Portfolio Title"
        _create_game_helper(game_title, "test rules", 10000)
        _post_portfolio_helper(portfolio_title, game_title)
        # WHEN
        _delete_portfolio_helper(portfolio_title, game_title)
        # THEN
        p = find_portfolio(portfolio_title, game_title)
        assert p is None

    def test_delete_portfolio_not_exist(self):
        """
        Test that deleting a portfolio that does not exit throws an exception
        """
        # GIVEN
        game_title = "Game Title"
        portfolio_title = "Portfolio Title"
        _create_game_helper(game_title, "test rules", 10000)
        # WHEN / THEN
        with self.assertRaises(Exception):
            _delete_portfolio_helper(portfolio_title, game_title)

    @mock.patch("api.helpers._buy_stock_helper", return_value=None)
    def test_trade_stock_helper_success_buy(self, mock_buy_stock):
        """
        Test that we buy a stock successfully if shares > 0
        """
        # GIVEN
        game_title = "Game Title"
        portfolio_title = "Portfolio Title"
        _create_game_helper(game_title, "test rules", 10000)
        _post_portfolio_helper(portfolio_title, game_title)
        ticker = "AAPL"
        shares = 3
        # WHEN
        _trade_stock_helper(portfolio_title, game_title, ticker, shares)
        # THEN
        portfolio = find_portfolio(portfolio_title, game_title)
        mock_buy_stock.assert_called_with(portfolio, ticker, shares)

    @mock.patch("api.helpers._sell_stock_helper")
    def test_trade_stock_helper_success_sell(self, mock_sell_stock):
        """
        Test that we sell a stock successfully if shares < 0
        """
        # GIVEN
        game_title = "Game Title"
        portfolio_title = "Portfolio Title"
        _create_game_helper(game_title, "test rules", 10000)
        _post_portfolio_helper(portfolio_title, game_title)
        ticker = "AAPL"
        shares = -3
        # WHEN
        _trade_stock_helper(portfolio_title, game_title, ticker, shares)
        # THEN
        portfolio = find_portfolio(portfolio_title, game_title)
        mock_sell_stock.assert_called_with(portfolio, ticker, shares)

    def test_trade_stock_helper_error(self):
        """
        Test that we cannot buy or sell a stock if portfolio does not exist
        """
        # GIVEN
        game_title = "Game Title"
        portfolio_title = "Portfolio Title"
        _create_game_helper(game_title, "test rules", 10000)
        # WHEN / THEN
        with self.assertRaises(Exception):
            _trade_stock_helper(portfolio_title, game_title, "AAPL", 3)

    @mock.patch("trade_simulation.models.Portfolio.buy_holding")
    def test_buy_stock_helper_success(self, buy_mock):
        """
        Test that buy stock helper works successfully
        """
        # GIVEN
        game_title = "Game Title"
        portfolio_title = "Portfolio Title"
        _create_game_helper(game_title, "test rules", 10000)
        _post_portfolio_helper(portfolio_title, game_title)
        ticker = "AAPL"
        shares = 3
        portfolio = find_portfolio(portfolio_title, game_title)
        # WHEN
        _buy_stock_helper(portfolio, ticker, shares)
        # THEN
        buy_mock.assert_called_with(ticker, shares)

    @mock.patch("trade_simulation.models.Portfolio.sell_holding")
    def test_sell_stock_helper_success(self, sell_mock):
        """
        Test that sell stock helper works successfully
        """
        # GIVEN
        game_title = "Game Title"
        portfolio_title = "Portfolio Title"
        _create_game_helper(game_title, "test rules", 10000)
        _post_portfolio_helper(portfolio_title, game_title)
        ticker = "AAPL"
        shares = -3
        portfolio = find_portfolio(portfolio_title, game_title)
        # WHEN
        _sell_stock_helper(portfolio, ticker, shares)
        # THEN
        sell_mock.assert_called_with(ticker, shares)

    def test_get_holding_helper_success(self):
        """
        Test that we can successfully get a holding for a portfolio
        """
        # GIVEN
        game_title = "Game Title"
        portfolio_title = "Portfolio Title"
        _create_game_helper(game_title, "test rules", 10000)
        _post_portfolio_helper(portfolio_title, game_title)
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
        game_title = "Game Title"
        portfolio_title = "Portfolio Title"
        _create_game_helper(game_title, "test rules", 10000)
        # WHEN / THEN
        with self.assertRaises(Exception):
            _get_holding_helper(portfolio_title, game_title, "AAPL")
