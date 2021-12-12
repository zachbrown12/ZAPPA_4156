from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .serializers import HoldingSerializer, OptionSerializer, TransactionSerializer, UserSerializer
from trade_simulation.models import Game, Portfolio, Holding, Option, Transaction
from .helpers import (
    _get_game_standings_helper,
    _get_game_helper,
    _create_game_helper,
    _delete_game_helper,
    _get_portfolios_helper,
    _get_portfolio_helper,
    _post_portfolio_helper,
    _delete_portfolio_helper,
    _trade_stock_helper,
    _trade_option_helper,
    _get_holding_helper,
    _get_option_helper,
)

GET_METHOD = "GET"
POST_METHOD = "POST"
DELETE_METHOD = "DELETE"

GAME_URL = "/api/game/game_title"
PORTFOLIO_URL = "/api/portfolio/game_title/port_title"


@api_view(["GET"])
def get_routes(request):
    """
    Function that stores all the routes and gets the appropriate route
    """
    routes = [
        {"GET": "/api/games"},
        {"GET": GAME_URL},
        {"POST": GAME_URL},
        {"DELETE": GAME_URL},
        {"GET": "/api/users"},
        {"POST": "/api/users"},
        {"GET": "/api/portfolios"},
        {"GET": PORTFOLIO_URL},
        {"POST": PORTFOLIO_URL},
        {"DELETE": PORTFOLIO_URL},
        {"POST": "/api/portfolio/trade"},
        {"GET": "/api/holdings"},
        {"GET": "/api/holding/port_title/game_title/ticker"},
        {"GET": "/api/options"},
        {"GET": "/api/option/port_title/game_title/contract"},
        {"GET": "/api/transactions"},
        {"GET": "/api/transaction/uid"},
    ]

    return Response(routes)


@api_view(["GET", "POST"])
def handle_users(request):
    if request.method == GET_METHOD:
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        user_response = serializer.data
        resp = Response(user_response)
        return resp
    elif request.method == POST_METHOD:
        username = request.data.get("username")
        password = request.data.get("password")
        user = User.objects.create_user(username=username, password=password)
        Token.objects.create(user=user)
        return Response()


@api_view(["GET"])
def handle_games(request):
    """
    Function that handles getting all created games
    """
    games = _get_game_standings_helper()
    resp = Response(games)
    return resp


@api_view(["GET", "POST", "DELETE"])
def handle_game(request, game_title):
    """
    Function that handles getting, creating, or deleting one game.
    """
    # On a GET request show the requested game or throw an error
    if request.method == GET_METHOD:
        try:
            data = _get_game_helper(game_title)
            return Response(data)
        except Exception as e:
            return Response(status=500, data=str(e))
    # On a POST request create the game or throw an error
    elif request.method == POST_METHOD:
        rules = request.data.get("rules")
        starting_balance = request.data.get("startingBalance")
        try:
            _create_game_helper(game_title, rules, starting_balance)
        except Exception as e:
            return Response(status=500, data=str(e))
        return Response()
    # On a DELETE request delete the game or throw an error
    elif request.method == DELETE_METHOD:
        try:
            data = _delete_game_helper(game_title)
            return Response(data)
        except Exception as e:
            return Response(status=500, data=str(e))


@api_view(["GET"])
def handle_portfolios(request):
    """
    Function that handles getting all portfolios
    """
    try:
        data = _get_portfolios_helper()
        return Response(data)
    except Exception as e:
        return Response(status=500, data=str(e))


@api_view(["GET", "POST", "DELETE"])
def handle_portfolio(request, game_title, port_title):
    """
    Function that handles getting, creating, or deleting one portfolio.
    """
    # On a GET request show the requested portfolio or throw an error
    if request.method == GET_METHOD:
        try:
            data = _get_portfolio_helper(port_title, game_title)
            return Response(data)
        except Exception as e:
            return Response(status=500, data=str(e))
    # On a POST request create the portfolio or throw an error
    elif request.method == POST_METHOD:
        try:
            if not (
                "username" in request.data and len(request.data.get("username")) > 0
            ):
                error = (
                    "Cannot create portfolio: username not found in body of request."
                )
                print(error)
                raise KeyError(error)
            username = request.data.get("username").lower()
            _post_portfolio_helper(port_title, game_title, username)
            return Response()
        except Exception as e:
            return Response(status=500, data=str(e))
    # On a DELETE request delete the portfolio or throw an error
    elif request.method == DELETE_METHOD:
        try:
            _delete_portfolio_helper(port_title, game_title)
            return Response()
        except Exception as e:
            return Response(status=500, data=str(e))


@api_view(["POST"])
def trade(request):
    """
    Function that handles buying or selling stock. This will update the transaction, holdings table.
    """
    portfolio_title = request.data.get("portfolioTitle")
    game_title = request.data.get("gameTitle")
    security_type = request.data.get("securityType")

    # If the trade type is a stock then set all the relevant data.
    if security_type == "stock":
        ticker = request.data.get("ticker")
        shares = request.data.get("shares")
        exercise = None
        if "exercise" in request.data:
            exercise = request.data.get("exercise")
        try:
            _trade_stock_helper(
                portfolio_title, game_title, ticker, shares, exercise=exercise
            )
        except Exception as e:
            return Response(status=500, data=str(e))
        return Response()

    # If the trade type is an option then set all the relevant data.
    elif security_type == "option":
        contract = request.data.get("contract")
        quantity = request.data.get("quantity")
        try:
            _trade_option_helper(portfolio_title, game_title, contract, quantity)
        except Exception as e:
            return Response(status=500, data=str(e))
        return Response()

    else:
        error = f"Option type {security_type} is not supported."
        print(error)
        return Response(status=500, data=str(error))


@api_view(["GET"])
def handle_holdings(request):
    """
    Function that handles getting all active holdings.
    """
    holdings = Holding.objects.all()
    serializer = HoldingSerializer(holdings, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def handle_holding(request, game_title, port_title, ticker):
    """
    Function that handles getting one holding within a portfolio
    """
    try:
        return Response(_get_holding_helper(port_title, game_title, ticker))
    except Exception as e:
        return Response(status=500, data=str(e))


@api_view(["GET"])
def handle_options(request):
    """
    Function that handles getting all active options.
    """
    options = Option.objects.all()
    serializer = OptionSerializer(options, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def handle_option(request, game_title, port_title, contract):
    """
    Function that handles getting one option within a portfolio
    """
    try:
        return Response(_get_option_helper(port_title, game_title, contract))
    except Exception as e:
        return Response(status=500, data=str(e))


@api_view(["GET"])
def handle_transactions(request):
    """
    Function that handles getting all transactions.
    """
    transactions = Transaction.objects.all()
    serializer = TransactionSerializer(transactions, many=True)
    print(f"Successfully fetched all transactions: {serializer.data}")
    return Response(serializer.data)


@api_view(["GET"])
def handle_transaction(request, pk):
    """
    Function that handles getting one particular transaction.
    """
    try:
        transaction = Transaction.objects.get(uid=pk)
    except Exception:
        return Response(status=500, data=f"Transaction with uid {pk} not found.")
    serializer = TransactionSerializer(transaction, many=False)
    print(f"Successfully fetched transaction: {serializer.data}")
    return Response(serializer.data)
