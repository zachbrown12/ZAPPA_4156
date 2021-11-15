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
    return Response(_get_game_standings_helper())


@api_view(["GET", "POST", "DELETE"])
def handle_game(request, game_title):
    if request.method == GET_METHOD:
        try:
            data = _get_game_helper(game_title)
            return Response(data)
        except Exception as e:
            return Response(status=500, data=e)
    elif request.method == POST_METHOD:
        rules = request.data.get("rules")
        starting_balance = request.data.get("starting_balance")
        try:
            _create_game_helper(game_title, rules, starting_balance)
        except Exception as e:
            return Response(status=500, data=e)
        return Response()
    elif request.method == DELETE_METHOD:
        try:
            data = _delete_game_helper(game_title)
            return Response(data)
        except Exception as e:
            return Response(status=500, data=e)


@api_view(["GET"])
def handle_portfolios(request):
    try:
        data = _get_portfolios_helper()
        return Response(data)
    except Exception as e:
        return Response(status=500, data=e)


@api_view(["GET", "POST", "DELETE"])
def handle_portfolio(request, game_title, port_title):
    if request.method == GET_METHOD:
        try:
            data = _get_portfolio_helper(port_title, game_title)
            return Response(data)
        except Exception as e:
            return Response(status=500, data=e)
    elif request.method == POST_METHOD:
        try:
            _post_portfolio_helper(port_title, game_title)
            return Response()
        except Exception as e:
            return Response(status=500, data=e)
    elif request.method == DELETE_METHOD:
        try:
            _delete_portfolio_helper(port_title, game_title)
            return Response()
        except Exception as e:
            return Response(status=500, data=e)


@api_view(["POST"])
def trade(request):
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
    holdings = Holding.objects.all()
    serializer = HoldingSerializer(holdings, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def handle_holding(request, game_title, port_title, ticker):
    return Response(_get_holding_helper(port_title, game_title, ticker))


@api_view(["GET"])
def handle_transactions(request):
    transactions = Transaction.objects.all()
    serializer = TransactionSerializer(transactions, many=True)
    print(f"Successfully fetched all transactions: {serializer.data}")
    return Response(serializer.data)


@api_view(["GET"])
def handle_transaction(request, pk):
    transaction = Transaction.objects.get(uid=pk)
    serializer = TransactionSerializer(transaction, many=False)
    print(f"Successfully fetched transaction: {serializer.data}")
    return Response(serializer.data)
