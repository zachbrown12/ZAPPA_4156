from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import GameSerializer, PortfolioSerializer, HoldingSerializer, TransactionSerializer
from trade_simulation.models import Game, Portfolio, Holding, Transaction
from .stockdata import ask_Price, bid_Price

@api_view(['GET'])
def getRoutes(request):

    routes = [
        {'GET':'/api/portfolios'},
        {'GET':'/api/portfolio/id'},
        {'POST':'/api/newportfolio'},
        {'POST':'/api/buystock/id'},
        {'POST':'/api/sellstock/id'},
        {'GET':'/api/holdings'},
        {'GET':'/api/holding/id'},
        {'GET':'/api/transactions'},
        {'GET':'/api/transaction/id'},
        {'GET':'/api/games'},
        {'GET':'/api/game/id'},
    ]

    return Response(routes)


@api_view(['GET'])
def getPortfolios(request):
    portfolios = Portfolio.objects.all()
    serializer = PortfolioSerializer(portfolios, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getPortfolio(request, pk):
    portfolio = Portfolio.objects.get()
    serializer = PortfolioSerializer(portfolio, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def makePortfolio(request):
    data = request.data
    portfolio = Portfolio.objects.create()
    portfolio.title = data['title']
    portfolio.save()
    return Response()


@api_view(['POST'])
def buyStock(request, pk):

    data = request.data
    portfolio = Portfolio.objects.get(id=pk)
    askprice = ask_Price(data['ticker'])

    #Code for updating holdings
    holding, created = Holding.objects.get_or_create(
        portfolio = portfolio,
        ticker = data['ticker']
    )

    cost = askprice * float(data['shares'])
    if float(portfolio.cash_balance) < cost:
        print("Not enough cash to buy ${} of {}.".format(
                    cost, data['ticker']))
        return Response()

    transaction = Transaction.objects.create()
    transaction.portfolio = portfolio
    transaction.ticker = data['ticker']
    transaction.tradeType = "Buy"
    transaction.shares = data['shares']
    transaction.bought_price = askprice
    transaction.save()

    holding.shares = (float(0 if holding.shares is None else holding.shares)
                      + float(data['shares']))
    holding.save()

    portfolio.cash_balance = float(portfolio.cash_balance) - cost
    portfolio.save()

    return Response()


@api_view(['POST'])
def sellStock(request, pk):

    data = request.data
    portfolio = Portfolio.objects.get(id=pk)
    bidprice = bid_Price(data['ticker'])

    #Code for updating holdings
    holding, created = Holding.objects.get_or_create(
        portfolio = portfolio,
        ticker = data['ticker']
    )

    currentshares = float(0 if holding.shares is None else holding.shares)
    if currentshares < float(data['shares']):
        print("Not enough shares of {} to sell {}.".format(
                        data['ticker'], float(data['shares'])))
        return Response()

    transaction = Transaction.objects.create()
    transaction.portfolio = portfolio
    transaction.ticker = data['ticker']
    transaction.tradeType = "Sell"
    transaction.shares = data['shares']
    transaction.bought_price = bidprice
    transaction.save()

    holding.shares = currentshares - float(data['shares'])
    holding.save()

    portfolio.cash_balance = float(portfolio.cash_balance) + (bidprice * 
                            float(data['shares']))
    portfolio.save()

    return Response()



@api_view(['GET'])
def getHoldings(request):
    holdings = Holding.objects.all()
    serializer = HoldingSerializer(holdings, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getHolding(request, pk):
    holding = Holding.objects.get()
    serializer = HoldingSerializer(holding, many=False)
    return Response(serializer.data)

@api_view(['GET'])
def getTransactions(request):
    transactions = Transaction.objects.all()
    serializer = TransactionSerializer(transactions, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getTransaction(request, pk):
    transaction = Transaction.objects.get()
    serializer = TransactionSerializer(transaction, many=False)
    return Response(serializer.data)

@api_view(['GET'])
def getGames(request):
    games = Game.objects.all()
    serializer = GameSerializer(games, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getGame(request, pk):
    game = Game.objects.get()
    serializer = GameSerializer(game, many=False)
    return Response(serializer.data)
