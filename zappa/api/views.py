from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import GameSerializer, PortfolioSerializer, HoldingSerializer, TransactionSerializer
from trade_simulation.models import Game, Portfolio, Holding, Transaction

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
    transaction = Transaction.objects.create()
    transaction.portfolio = portfolio
    transaction.ticker = data['ticker']
    transaction.tradeType = "Buy"
    transaction.shares = data['shares']

    ### This is hard coded. An API call needs to happen here
    transaction.bought_price = 10.00
    transaction.save()

    #Code for updating holdings
    holding, created = Holding.objects.get_or_create(
        portfolio = portfolio,
        ticker = data['ticker']
    )

    holding.portfolio = portfolio
    holding.ticker = data['ticker']
    holding.shares = float(0 if holding.shares is None else holding.shares) + float(data['shares'])
    ### This is hard coded. An API call needs to happen here
    holding.current_price  = 10.00
    holding.save()

    portfolio.cash_balance = float(portfolio.cash_balance) - (holding.current_price * 
                            float(data['shares']))
    portfolio.save()

    return Response()


@api_view(['POST'])
def sellStock(request, pk):

    data = request.data
    portfolio = Portfolio.objects.get(id=pk)
    transaction = Transaction.objects.create()
    transaction.portfolio = portfolio
    transaction.ticker = data['ticker']
    transaction.tradeType = "Sell"
    transaction.shares = data['shares']

    ### This is hard coded. An API call needs to happen here
    transaction.bought_price = 10.00
    transaction.save()

    #Code for updating holdings
    holding, created = Holding.objects.get_or_create(
        portfolio = portfolio,
        ticker = data['ticker']
    )

    holding.portfolio = portfolio
    holding.ticker = data['ticker']
    holding.shares = float(0 if holding.shares is None else holding.shares) - float(data['shares'])
    ### This is hard coded. An API call needs to happen here
    holding.current_price  = 10.00
    holding.save()

    portfolio.cash_balance = float(portfolio.cash_balance) + (holding.current_price * 
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
