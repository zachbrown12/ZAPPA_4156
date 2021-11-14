from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import (
    GameSerializer,
    PortfolioSerializer,
    HoldingSerializer,
    TransactionSerializer,
)
from trade_simulation.models import Game, Portfolio, Holding, Transaction

GET_METHOD = "GET"
POST_METHOD = "POST"
DELETE_METHOD = "DELETE"


@api_view(["GET"])
def getRoutes(request):

    routes = [
        {"GET": "/api/games"},
        {"POST": "/api/games"},
        {"DELETE": "/api/games"},
        {"GET": "/api/portfolios/"},
        {"POST": "/api/portfolios/"},
        {"GET": "/api/portfolio/portfolio_id"},
        {"DELETE": "/api/portfolio/portfolio_id"},
        {"POST": "/api/portfolio/portfolio_id/buy/stock/ticker"},
        {"POST": "/api/portfolio/portfolio_id/sell/stock/ticker"},
        {"GET": "/api/holdings"},
        {"GET": "/api/holding/id"},
        {"GET": "/api/transactions"},
        {"GET": "/api/transaction/id"},
    ]

    return Response(routes)


@api_view(["GET", "POST", "DELETE"])
def handle_games(request):
    if request.method == GET_METHOD:
        return Response(_get_game_standings_helper())
    elif request.method == POST_METHOD:
        _create_game_helper(request.data)
        return Response()
    elif request.method == DELETE_METHOD:
        return Response(_delete_game_helper(request.data))


# TODO:support multiple games
def _get_game_standings_helper():
    game = Game.objects.all()
    if len(game) <= 0:
        return None
    game = game[0]  # Assumes only one game at a time
    game.rankPortfolios()
    serializer = GameSerializer(game, many=False)
    print(f"Returning game standings: {serializer.data}")
    return serializer.data


def _create_game_helper(data):
    # title is a unique field
    if Game.objects.filter(title=data.get("title")).exists():
        print("game with same name existed")
        return

    game = Game.objects.create()
    game.title = data.get("title")
    game.rules = data.get("rules")
    if data.get("startingBalance"):
        game.startingBalance = float(data.get("startingBalance"))
    game.save()
    print("Successfully created new game")


def _delete_game_helper(data):
    try:
        game = Game.objects.get(data.get("title"))
        game.delete()
        print(f"Successfully deleted game {game.title}")
    except Game.DoesNotExist:
        print(
            "Could not find game with name {}.".format(
                data.get("title")
            )
        )


@api_view(["GET", "POST"])
def handle_portfolios(request):
    if request.method == GET_METHOD:
        return Response(_get_portfolio_helper())
    elif request.method == POST_METHOD:
        _post_portfolio_helper(request.data)
        return Response()


@api_view(["GET", "DELETE"])
def handle_portfolio_pk(request, pk):
    if request.method == GET_METHOD:
        return Response(_get_portfolio_pk_helper(pk))
    elif request.method == DELETE_METHOD:
        _delete_portfolio_pk_helper(pk)
        return Response()


def _get_portfolio_pk_helper(portfolio_id):
    portfolio = Portfolio.objects.get(id=portfolio_id)
    portfolio.computeTotalValue()
    serializer = PortfolioSerializer(portfolio, many=False)
    print(f"Fetched portfolio with id={portfolio_id}: {serializer.data}")
    return serializer.data


def _delete_portfolio_pk_helper(portfolio_id):
    try:
        portfolio = Portfolio.objects.get(id=portfolio_id)
        portfolio.delete()
        print(f"Successfully deleted portfolio with id={portfolio_id}")
    except Portfolio.DoesNotExist:
        print(
            "Could not find portfolio ID {}.".format(
                portfolio_id
            )
        )


def _get_portfolio_helper():
    portfolios = Portfolio.objects.all()
    for portfolio in portfolios:
        portfolio.computeTotalValue()
    serializer = PortfolioSerializer(portfolios, many=True)
    print(f"Successfullly fetched all portfolios: {serializer.data}")
    return serializer.data


def _post_portfolio_helper(data):
    game = None

    try:
        game = Game.objects.get(title=data.get("gameTitle"))
    except Game.DoesNotExist:
        print(
            "Could not find game with name {}.".format(
                data.get("gameTitle")
            )
        )
        return

    if Portfolio.objects.filter(title=data.get("title"), game=game).exists():
        print(
            "Portfolio named {} is already in game {}.".format(
                data.get("title"), data.get("gameTitle")
            )
        )
        return

    portfolio = Portfolio.objects.create()
    portfolio.game = game
    portfolio.cash_balance = float(game.startingBalance)
    portfolio.total_value = float(game.startingBalance)
    portfolio.title = data.get("title")
    portfolio.save()
    print(f"Successfully created new portfolio with title={data.get('title')}")


@api_view(["POST"])
def buy(request, pk, ticker):
    _buy_stock_helper(pk, ticker, request.data)
    return Response()


def _buy_stock_helper(portfolio_id, ticker, data):
    portfolio = Portfolio.objects.get(id=portfolio_id)
    portfolio.buyHolding(ticker, data.get("shares"))
    print(
        f"Portfolio id={portfolio_id} purchased {data.get('shares')} shares of {ticker}"
    )


@api_view(["POST"])
def sell(request, pk, ticker):
    _sell_stock_helper(pk, ticker, request.data)
    return Response()


def _sell_stock_helper(portfolio_id, ticker, data):
    portfolio = Portfolio.objects.get(id=portfolio_id)
    portfolio.sellHolding(ticker, data.get("shares"))
    print(f"Portfolio id={portfolio_id} sold {data.get('shares')} shares of {ticker}")


@api_view(["GET"])
def handle_holdings(request):
    holdings = Holding.objects.all()
    serializer = HoldingSerializer(holdings, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def handle_holding(request, pk):
    holding = Holding.objects.get(id=pk)
    serializer = HoldingSerializer(holding, many=False)
    print(f"Successfully fetched holding id={pk}: {serializer.data}")
    return Response(serializer.data)


@api_view(["GET"])
def handle_transactions(request):
    transactions = Transaction.objects.all()
    serializer = TransactionSerializer(transactions, many=True)
    print(f"Successfully fetched all transactions: {serializer.data}")
    return Response(serializer.data)


@api_view(["GET"])
def handle_transaction(request, pk):
    transaction = Transaction.objects.get(id=pk)
    serializer = TransactionSerializer(transaction, many=False)
    print(f"Successfully fetched transaction: {serializer.data}")
    return Response(serializer.data)
