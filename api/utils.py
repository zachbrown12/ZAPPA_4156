from trade_simulation.models import Game, Portfolio, Holding
from django.contrib.auth.models import User


def find_game_by_title(title):
    """
    Function that runs a query on the database to find one game.
    """
    try:
        game = Game.objects.get(title=title)
        return game
    except Game.DoesNotExist:
        print(f"No game found by name {title}")
        return None


def find_portfolio(title, game_title):
    """
    Function that runs a query on the database to find one portfolio
    """
    game = find_game_by_title(game_title)
    if not game:
        return
    try:
        portfolio = Portfolio.objects.get(title=title, game=game)
        return portfolio
    except Portfolio.DoesNotExist:
        print(f"No portfolio named {title} found in game {game_title}")
        return None


def find_holding(title, game_title, ticker):
    """
    Function that runs a query on the database to find one holding.
    """
    portfolio = find_portfolio(title, game_title)
    if not portfolio:
        return
    try:
        holding = Holding.objects.get(portfolio=portfolio, ticker=ticker)
        return holding
    except Holding.DoesNotExist:
        print(f"No holding of ticker {ticker} in portfolio {title}.")
        return None


def find_user_by_username(username):
    """
    Function that runs a query on the database to find user by username
    """
    try:
        user = User.objects.get(username=username)
        return user
    except User.DoesNotExist:
        print(f"No user found by username {username}")
        return None
