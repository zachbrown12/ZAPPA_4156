from .serializers import GameSerializer, PortfolioSerializer, HoldingSerializer, OptionSerializer
from trade_simulation.models import Game, Portfolio, Holding, Option
from .utils import find_game_by_title, find_portfolio, find_holding, find_option


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
        error = f"Could not find game with title {game_title}."
        print(error)
        raise Exception(error)
    game.rank_portfolios()
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
        error = f"Game with title {title} already exists."
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
        error = f"Error occurs when creating the game {title}."
        print(error)
        raise Exception(error)


def _delete_game_helper(title):
    """
    Helper function to delete a game by title
    Returns: N/A or error
    """
    game = find_game_by_title(title)
    if not game:
        error = f"Could not find game with title {title}."
        print(error)
        raise Exception(error)
    try:
        game.delete()
        print(f"Successfully deleted game {game.title}.")
    except Game.DoesNotExist:
        error = f"Error occurs when deleting the game {game.title}."
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
        print(f"Successfully fetched all portfolios: {serializer.data}.")
        return serializer.data
    except RuntimeError:
        error = "Error occurs when fetching all portfolios."
        print(error)
        raise Exception(error)


def _get_portfolio_helper(title, game_title):
    """
    Helper function to return specific portfolio in specific game
    Returns: Portfolio object
    """
    portfolio = find_portfolio(title, game_title)
    if not portfolio:
        error = f"Could not find portfolio with title {title} in game {game_title}."
        print(error)
        raise Exception(error)
    try:
        # Compute total value to make sure portfolio object is up to date
        portfolio.compute_total_value()
        serializer = PortfolioSerializer(portfolio, many=False)
        print(f"Fetched portfolio with id={portfolio.uid}: {serializer.data}")
        return serializer.data
    except RuntimeError:
        error = "Error occurs when serializing the portfolio."
        print(error)
        raise Exception(error)


def _delete_portfolio_helper(title, game_title):
    """
    Helper function to delete specific portfolio in specific game
    Returns: N/A or error
    """
    portfolio = find_portfolio(title, game_title)
    if not portfolio:
        error = f"Portfolio {title} in game {game_title} cannot be deleted as it does not exist."
        print(error)
        raise Exception(error)
    try:
        portfolio.delete()
        print("Successfully deleted portfolio.")
    except RuntimeError:
        error = "Error occurs when serializing the portfolio."
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
            f"Successfully created new portfolio with title {title} in game {game_title}."
        )
    except RuntimeError:
        error = "Error occurs when creating/saving portfolio."
        print(error)
        raise Exception(error)


def _trade_stock_helper(title, game_title, ticker, shares, exercise=None):
    """
    Helper function to buy or sell a stock
    Returns: N/A
    """
    portfolio = find_portfolio(title, game_title)
    print("portfolio here")
    print(portfolio)
    if not portfolio:
        error = f"Cannot find portfolio {title} in game {game_title}."
        print(error)
        raise Exception(error)
    if shares > 0:
        portfolio.buy_holding(ticker, shares, exercise=exercise)
        print(f"Portfolio {title} purchased {shares} shares of {ticker}.")
        if exercise:
            print(f"Exercised option {exercise}.")
    elif shares < 0:
        portfolio.sell_holding(ticker, -shares, exercise=exercise)
        print(f"Portfolio {title} sold {-shares} shares of {ticker}.")
        if exercise:
            print(f"Exercised option {exercise}.")


def _trade_option_helper(title, game_title, contract, quantity):
    """
    Helper function to buy or sell an option
    Returns: N/A
    """
    portfolio = find_portfolio(title, game_title)
    print("portfolio here")
    print(portfolio)
    if not portfolio:
        error = f"Cannot find portfolio {title} in game {game_title}."
        print(error)
        raise Exception(error)
    if quantity > 0:
        portfolio.buy_option(contract, quantity)
        print(f"Portfolio {title} purchased {quantity} options of {contract}.")
    elif quantity < 0:
        portfolio.sell_option(contract, -quantity)
        print(f"Portfolio {title} sold {-quantity} options of {contract}.")


def _get_holding_helper(portfolio_title, game_title, ticker):
    """
    Helper function to fetch a particular holding in a portfolio
    Returns: Holding data or error
    """
    portfolio = find_portfolio(portfolio_title, game_title)
    if not portfolio:
        error = f"Cannot find portfolio {portfolio_title} in game {game_title}."
        print(error)
        raise Exception(error)
    holding = find_holding(portfolio_title, game_title, ticker)
    if not holding:
        error = f"Cannot find holding {ticker} in portfolio {portfolio_title} in game {game_title}."
        print(error)
        raise Exception(error)
    try:
        serializer = HoldingSerializer(holding, many=False)
        print(f"Successfully fetched holding id={holding.uid}: {serializer.data}")
        return serializer.data
    except Holding.DoesNotExist:
        error = "Error occurs when serializing the holdings in portfolio."
        print(error)
        raise Exception(error)


def _get_option_helper(portfolio_title, game_title, contract):
    """
    Helper function to fetch a particular holding in a portfolio
    Returns: Holding data or error
    """
    portfolio = find_portfolio(portfolio_title, game_title)
    if not portfolio:
        error = f"Cannot find portfolio {portfolio_title} in game {game_title}."
        print(error)
        raise Exception(error)
    option = find_option(portfolio_title, game_title, contract)
    if not option:
        error = f"Cannot find option {contract} in portfolio {portfolio_title} in game {game_title}."
        print(error)
        raise Exception(error)
    try:
        serializer = OptionSerializer(option, many=False)
        print(f"Successfully fetched option id={option.uid}: {serializer.data}")
        return serializer.data
    except Option.DoesNotExist:
        error = "Error occurs when serializing the options in portfolio."
        print(error)
        raise Exception(error)
