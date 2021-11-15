from .serializers import (
    GameSerializer,
    PortfolioSerializer,
    HoldingSerializer,
)
from trade_simulation.models import Game, Portfolio, Holding
from .utils import find_game_by_title, find_portfolio, find_holding


def _get_game_standings_helper():
    games = Game.objects.all()
    if len(games) <= 0:
        return None
    for game in games:
        game.rank_portfolios()
    serializer = GameSerializer(games, many=True)
    print(f"Returning game standings: {serializer.data}.")
    return serializer.data


def _get_game_helper(game_title):
    game = find_game_by_title(game_title)
    if not game:
        return
    try:
        serializer = GameSerializer(game, many=False)
        print(f"Returning game standings: {serializer.data}.")
        return serializer.data
    except RuntimeError:
        print("Error occurs when serializing the game.")


def _create_game_helper(title, rules, starting_balance):
    # title is a unique field
    if Game.objects.filter(title=title).exists():
        print("game with same name existed.")
        return

    try:
        game = Game.objects.create()
        game.title = title
        game.rules = rules
        if starting_balance:
            game.starting_balance = float(starting_balance)
        game.save()
        print("Successfully created new game.")
    except RuntimeError:
        print("Error occurs when creating the game.")


def _delete_game_helper(title):
    game = find_game_by_title(title)
    if not game:
        return
    try:
        game.delete()
        print(f"Successfully deleted game {game.title}")
    except Game.DoesNotExist:
        print("Error occurs when deleting the game.")


def _get_portfolios_helper():
    try:
        portfolios = Portfolio.objects.all()
        for portfolio in portfolios:
            portfolio.compute_total_value()
        serializer = PortfolioSerializer(portfolios, many=True)
        print(f"Successfullly fetched all portfolios: {serializer.data}.")
        return serializer.data
    except RuntimeError:
        print("Error occurs when fetched all portfolios.")


def _get_portfolio_helper(title, game_title):
    portfolio = find_portfolio(title, game_title)
    if not portfolio:
        return
    try:
        portfolio.compute_total_value()
        serializer = PortfolioSerializer(portfolio, many=False)
        print(f"Fetched portfolio with id={portfolio.uid}: {serializer.data}")
        return serializer.data
    except RuntimeError:
        print("Error occurs when serialize the portfolio.")


def _delete_portfolio_helper(title, game_title):
    portfolio = find_portfolio(title, game_title)
    if not portfolio:
        return
    try:
        portfolio.delete()
        print("Successfully deleted portfolio.")
    except RuntimeError:
        print("Error occurs when serialize the portfolio.")


def _post_portfolio_helper(title, game_title):
    game = find_game_by_title(game_title)
    if not game:
        print(f"No game named {game_title}.")
        return

    if Portfolio.objects.filter(title=title, game=game).exists():
        print(f"Portfolio named {title} is already in game {game_title}.")
        return

    try:
        portfolio = Portfolio.objects.create()
        portfolio.game = game
        portfolio.cash_balance = float(game.starting_balance)
        portfolio.total_value = float(game.starting_balance)
        portfolio.title = title
        portfolio.save()
        print(f"Successfully created new portfolio with title={title} in game {game_title}")
    except RuntimeError:
        print("Error occurs when creating/saving portfolio.")


def _trade_stock_helper(title, game_title, ticker, shares):
    portfolio = find_portfolio(title, game_title)
    if not portfolio:
        print("Cannot find portfolio")
    if shares > 0:
        _buy_stock_helper(portfolio, ticker, shares)
    elif shares < 0:
        _sell_stock_helper(portfolio, ticker, shares)


# TODO:combining sellholding and buyholding
def _buy_stock_helper(portfolio, ticker, shares):
    portfolio.buy_holding(ticker, shares)
    print(f"Portfolio id={portfolio.uid} purchased {shares} shares of {ticker}")


# TODO:combining sellholding and buyholding
def _sell_stock_helper(portfolio, ticker, shares):
    portfolio.sell_holding(ticker, -shares)
    print(f"Portfolio id={portfolio.uid} sold {shares} shares of {ticker}")


def _get_holding_helper(portfolio_title, game_title, ticker):
    portfolio = find_portfolio(portfolio_title, game_title)
    if not portfolio:
        return
    holding = find_holding(portfolio_title, game_title, ticker)
    try:
        serializer = HoldingSerializer(holding, many=False)
        print(f"Successfully fetched holding id={holding.uid}: {serializer.data}")
        return serializer.data
    except Holding.DoesNotExist:
        print("Error occurs when serialize the holding portfolio.")
        return
