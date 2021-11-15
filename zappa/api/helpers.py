from .serializers import GameSerializer, PortfolioSerializer, HoldingSerializer
from trade_simulation.models import Game, Portfolio, Holding
from .utils import find_game_by_title, find_portfolio, find_holding


def _get_game_standings_helper():
    """
    Helper function to fetch portfolio rankings for each game
    Returns: Game objects with winners set
    """
    games = Game.objects.all()
    if len(games) <= 0:
        return None
    for game in games:
        game.rank_portfolios()
    serializer = GameSerializer(games, many=True)
    print(f"Returning game standings: {serializer.data}.")
    return serializer.data


def _get_game_helper(game_title):
    """
    Helper function to find and return game
    Returns: game with title game_title or error
    """
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


def _create_game_helper(title, rules, starting_balance):
    """
    Helper function to create a new game
    Returns: N/A or error
    """
    # title is a unique field
    if Game.objects.filter(title=title).exists():
        error = "Game with same name already exists."
        print(error)
        raise Exception(error)

    try:
        game = Game.objects.create()
        game.title = title
        game.rules = rules
        if starting_balance:
            game.starting_balance = float(starting_balance)
        game.save()
        print("Successfully created new game.")
    except RuntimeError:
        error = "Error occurs when creating the game."
        print(error)
        raise Exception(error)


def _delete_game_helper(title):
    """
    Helper function to delete a game by title
    Returns: N/A or error
    """
    game = find_game_by_title(title)
    if not game:
        error = "Error occurs when deleting the game."
        print(error)
        raise Exception(error)
    try:
        game.delete()
        print(f"Successfully deleted game {game.title}")
    except Game.DoesNotExist:
        error = "Error occurs when deleting the game."
        print(error)
        raise Exception(error)


def _get_portfolios_helper():
    """
    Helper function to get all portfolios in all games
    Returns: portfolio objects
    """
    try:
        portfolios = Portfolio.objects.all()
        for portfolio in portfolios:
            # Compute total value to make sure portfolio object is up to date
            portfolio.compute_total_value()
        serializer = PortfolioSerializer(portfolios, many=True)
        print(f"Successfullly fetched all portfolios: {serializer.data}.")
        return serializer.data
    except RuntimeError:
        error = "Error occurs when fetched all portfolios."
        print(error)
        raise Exception(error)


def _get_portfolio_helper(title, game_title):
    """
    Helper function to return specific portfolio in specific game
    Returns: Portfolio object
    """
    portfolio = find_portfolio(title, game_title)
    if not portfolio:
        error = f"Could not get portfolio with title={title}"
        print(error)
        raise Exception(error)
    try:
        # Compute total value to make sure portfolio object is up to date
        portfolio.compute_total_value()
        serializer = PortfolioSerializer(portfolio, many=False)
        print(f"Fetched portfolio with id={portfolio.uid}: {serializer.data}")
        return serializer.data
    except RuntimeError:
        error = "Error occurs when serialize the portfolio."
        print(error)
        raise Exception(error)


def _delete_portfolio_helper(title, game_title):
    """
    Helper function to delete specific portfolio in specific game
    Returns: N/A or error
    """
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
    """
    Helper function to create a new portfolio
    Returns: N/A or error
    """
    game = find_game_by_title(game_title)
    if not game:
        error = f"No game named {game_title}."
        print(error)
        raise Exception(error)

    if Portfolio.objects.filter(title=title, game=game).exists():
        # We can only have one portfolio with a specific title in each game
        error = f"Portfolio named {title} is already in game {game_title}."
        print(error)
        raise Exception(error)

    try:
        portfolio = Portfolio.objects.create()
        portfolio.game = game
        portfolio.cash_balance = float(game.starting_balance)
        portfolio.total_value = float(game.starting_balance)
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
    """
    Helper function to buy or sell a stock
    Returns: N/A
    """
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
    """
    Helper function to buy a holding
    Returns: N/A
    """
    portfolio.buy_holding(ticker, shares)
    print(f"Portfolio id={portfolio.uid} purchased {shares} shares of {ticker}")


# TODO:combining sellholding and buyholding
def _sell_stock_helper(portfolio, ticker, shares):
    """
    Helper function to sell a holding
    Returns: N/A
    """
    portfolio.sell_holding(ticker, -shares)
    print(f"Portfolio id={portfolio.uid} sold {shares} shares of {ticker}")


def _get_holding_helper(portfolio_title, game_title, ticker):
    """
    Helper function to fetch a particular holding in a portfolio
    Returns: Holding data or error
    """
    portfolio = find_portfolio(portfolio_title, game_title)
    if not portfolio:
        return
    holding = find_holding(portfolio_title, game_title, ticker)
    try:
        serializer = HoldingSerializer(holding, many=False)
        print(f"Successfully fetched holding id={holding.uid}: {serializer.data}")
        return serializer.data
    except Holding.DoesNotExist:
        error = "Error occurs when serialize the holding portfolio."
        print(error)
        raise Exception(error)
