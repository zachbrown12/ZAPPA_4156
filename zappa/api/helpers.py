from .serializers import GameSerializer, PortfolioSerializer, HoldingSerializer
from trade_simulation.models import Game, Portfolio, Holding
from .utils import find_game_by_title, find_portfolio, find_holding


def _get_game_standings_helper():
    games = Game.objects.all()
    if len(games) <= 0:
        return None
    for game in games:
        game.rankPortfolios()
    serializer = GameSerializer(games, many=True)
    print(f"Returning game standings: {serializer.data}.")
    return serializer.data


def _get_game_helper(game_title):
    game = find_game_by_title(game_title)
    if not game:
        error = "Could not find game"
        print(error)
        raise Exception(error)
    try:
        serializer = GameSerializer(game, many=False)
        print(f"Returning game standings: {serializer.data}.")
        return serializer.data
    except RuntimeError:
        error = "Error occurs when serializing the game."
        print(error)
        raise Exception(error)


def _create_game_helper(title, rules, startingBalance):
    # title is a unique field
    if Game.objects.filter(title=title).exists():
        print("game with same name existed.")
        return

    try:
        game = Game.objects.create()
        game.title = title
        game.rules = rules
        if startingBalance:
            game.startingBalance = float(startingBalance)
        game.save()
        print("Successfully created new game.")
    except RuntimeError:
        error = "Error occurs when creating the game."
        print(error)
        raise Exception(error)


def _delete_game_helper(title):
    game = find_game_by_title(title)
    if not game:
        return
    try:
        game.delete()
        print(f"Successfully deleted game {game.title}")
    except Game.DoesNotExist:
        error = "Error occurs when deleting the game."
        print(error)
        raise Exception(error)


def _get_portfolios_helper():
    try:
        portfolios = Portfolio.objects.all()
        for portfolio in portfolios:
            portfolio.computeTotalValue()
        serializer = PortfolioSerializer(portfolios, many=True)
        print(f"Successfullly fetched all portfolios: {serializer.data}.")
        return serializer.data
    except RuntimeError:
        error = "Error occurs when fetched all portfolios."
        print(error)
        raise Exception(error)


def _get_portfolio_helper(title, game_title):
    portfolio = find_portfolio(title, game_title)
    if not portfolio:
        return
    try:
        portfolio.computeTotalValue()
        serializer = PortfolioSerializer(portfolio, many=False)
        print(f"Fetched portfolio with id={portfolio.id}: {serializer.data}")
        return serializer.data
    except RuntimeError:
        error = "Error occurs when serialize the portfolio."
        print(error)
        raise Exception(error)


def _delete_portfolio_helper(title, game_title):
    portfolio = find_portfolio(title, game_title)
    if not portfolio:
        return
    try:
        portfolio.delete()
        print("Successfully deleted portfolio.")
    except RuntimeError:
        error = "Error occurs when serialize the portfolio."
        print(error)
        raise Exception(error)


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
        portfolio.cash_balance = float(game.startingBalance)
        portfolio.total_value = float(game.startingBalance)
        portfolio.title = title
        portfolio.save()
        print(
            f"Successfully created new portfolio with title={title} in game {game_title}"
        )
    except RuntimeError:
        error = "Error occurs when creating/saving portfolio."
        print(error)
        raise Exception(error)


def _trade_stock_helper(title, game_title, ticker, shares):
    portfolio = find_portfolio(title, game_title)
    if not portfolio:
        error = f"Cannot find portfolio {title}"
        print(error)
        raise Exception(error)
    if shares > 0:
        _buy_stock_helper(portfolio, ticker, shares)
    elif shares < 0:
        _sell_stock_helper(portfolio, ticker, shares)


# TODO:combining sellholding and buyholding
def _buy_stock_helper(portfolio, ticker, shares):
    portfolio.buyHolding(ticker, shares)
    print(f"Portfolio id={portfolio.id} purchased {shares} shares of {ticker}")


# TODO:combining sellholding and buyholding
def _sell_stock_helper(portfolio, ticker, shares):
    portfolio.sellHolding(ticker, -shares)
    print(f"Portfolio id={portfolio.id} sold {shares} shares of {ticker}")


def _get_holding_helper(portfolio_title, game_title, ticker):
    portfolio = find_portfolio(portfolio_title, game_title)
    if not portfolio:
        return
    holding = find_holding(portfolio_title, game_title, ticker)
    try:
        serializer = HoldingSerializer(holding, many=False)
        print(f"Successfully fetched holding id={holding.id}: {serializer.data}")
        return serializer.data
    except Holding.DoesNotExist:
        error = "Error occurs when serialize the holding portfolio."
        print(error)
        raise Exception(error)