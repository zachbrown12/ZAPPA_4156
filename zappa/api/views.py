from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import (
    GameSerializer,
    PortfolioSerializer,
    StockSerializer,
    TransactionSerializer,
)
from trade_simulation.models import Game, Portfolio, Stock, Transaction


@api_view(["GET"])
def getRoutes(request):

    routes = [
        {"GET": "/api/portfolios"},
        {"GET": "/api/portfolio/id"},
        {"GET": "/api/stocks"},
        {"GET": "/api/stock/id"},
        {"GET": "/api/transactions"},
        {"GET": "/api/transaction/id"},
        {"GET": "/api/games"},
        {"GET": "/api/game/id"},
    ]

    return Response(routes)


@api_view(["GET"])
def getGames(request):
    games = Game.objects.all()
    serializer = GameSerializer(games, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def getGame(request, pk):
    game = Game.objects.get()
    serializer = GameSerializer(game, many=False)
    return Response(serializer.data)


@api_view(["GET"])
def getPortfolios(request):
    portfolios = Portfolio.objects.all()
    serializer = PortfolioSerializer(portfolios, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def getPortfolio(request, pk):
    portfolio = Portfolio.objects.get()
    serializer = PortfolioSerializer(portfolio, many=False)
    return Response(serializer.data)


@api_view(["GET"])
def getStocks(request):
    stocks = Stock.objects.all()
    serializer = StockSerializer(stocks, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def getStock(request, pk):
    stock = Stock.objects.get()
    serializer = StockSerializer(stock, many=False)
    return Response(serializer.data)


@api_view(["GET"])
def getTransactions(request):
    transactions = Transaction.objects.all()
    serializer = TransactionSerializer(transactions, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def getTransaction(request, pk):
    transaction = Transaction.objects.get()
    serializer = TransactionSerializer(transaction, many=False)
    return Response(serializer.data)
