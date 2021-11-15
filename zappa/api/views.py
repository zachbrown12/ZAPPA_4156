from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import HoldingSerializer, TransactionSerializer
from trade_simulation.models import Game, Portfolio, Holding, Transaction
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
    _get_holding_helper,
)

GET_METHOD = "GET"
POST_METHOD = "POST"
DELETE_METHOD = "DELETE"


@api_view(["GET"])
def getRoutes(request):
    """
    Function that stores all the routes and gets the appropriate route
    """
    routes = [
        {"GET": "/api/games"},
        {"GET": "/api/game/game_title"},
        {"POST": "/api/game/game_title"},
        {"DELETE": "/api/game/game_title"},
        {"GET": "/api/portfolios"},
        {"GET": "/api/portfolio/game_title/port_title"},
        {"POST": "/api/portfolio/game_title/port_title"},
        {"DELETE": "/api/portfolio/game_title/port_title"},
        {"POST": "/api/portfolio/trade"},
        {"GET": "/api/holdings"},
        {"GET": "/api/holding/port_title/game_title/ticker"},
        {"GET": "/api/transactions"},
        {"GET": "/api/transaction/uid"},
    ]

    return Response(routes)


@api_view(["GET"])
def handle_games(request):
    """
    Function that handles getting all created games
    """
    return Response(_get_game_standings_helper())


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
            return Response(status=500, data=e)
    # On a POST request create the game or throw an error
    elif request.method == POST_METHOD:
        rules = request.data.get("rules")
        starting_balance = request.data.get("startingBalance")
        try:
            _create_game_helper(game_title, rules, starting_balance)
        except Exception as e:
            return Response(status=500, data=e)
        return Response()
    # On a DELETE request delete the game or throw an error
    elif request.method == DELETE_METHOD:
        try:
            data = _delete_game_helper(game_title)
            return Response(data)
        except Exception as e:
            return Response(status=500, data=e)


@api_view(["GET"])
def handle_portfolios(request):
    """
    Function that handles getting all portfolios
    """
    try:
        data = _get_portfolios_helper()
        return Response(data)
    except Exception as e:
        return Response(status=500, data=e)


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
            return Response(status=500, data=e)
    # On a POST request create the portfolio or throw an error
    elif request.method == POST_METHOD:
        try:
            _post_portfolio_helper(port_title, game_title)
            return Response()
        except Exception as e:
            return Response(status=500, data=e)
    # On a DELETE request delete the portfolio or throw an error
    elif request.method == DELETE_METHOD:
        try:
            _delete_portfolio_helper(port_title, game_title)
            return Response()
        except Exception as e:
            return Response(status=500, data=e)


@api_view(["POST"])
def trade(request):
    """
    Function that handles buying or selling stock. This will update the transaction, holdings table.
    """
    # If the trade type is a stock then set all the relevant data.
    securityType = request.data.get("securityType")
    if securityType == "stock":
        portfolio_title = request.data.get("portfolioTitle")
        game_title = request.data.get("gameTitle")
        ticker = request.data.get("ticker")
        shares = request.data.get("shares")
        try:
            _trade_stock_helper(portfolio_title, game_title, ticker, shares)
        except Exception as e:
            return Response(status=500, data=e)
    return Response()


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
    return Response(_get_holding_helper(port_title, game_title, ticker))


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
    transaction = Transaction.objects.get(uid=pk)
    serializer = TransactionSerializer(transaction, many=False)
    print(f"Successfully fetched transaction: {serializer.data}")
    return Response(serializer.data)
