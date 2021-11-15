from rest_framework.decorators import api_view
from rest_framework.response import Response
<<<<<<< HEAD
from .serializers import GameSerializer, PortfolioSerializer, HoldingSerializer, TransactionSerializer
from trade_simulation.models import Game, Portfolio, Holding, Transaction
=======
from .serializers import (
    HoldingSerializer,
    TransactionSerializer,
)
from trade_simulation.models import Game, Portfolio, Holding, Transaction
from .helpers import (
    _get_game_standings_helper,
>>>>>>> fccaa93827e74133b204f7335c73749de893625a

    _get_game_helper,
    _create_game_helper,
    _delete_game_helper,

    _get_portfolios_helper,
    _get_portfolio_helper,
    _post_portfolio_helper,
    _delete_portfolio_helper,

    _trade_stock_helper,
    _get_holding_helper
)

GET_METHOD = "GET"
POST_METHOD = "POST"
DELETE_METHOD = "DELETE"


@api_view(["GET"])
def getRoutes(request):

    routes = [
<<<<<<< HEAD
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
=======
        {"GET": "/api/games"},
        {"POST": "/api/game/game_title"},
        {"DELETE": "/api/game/game_title"},

        {"GET": "/api/portfolios"},

        {"GET": "/api/portfolio/game_title/port_title"},
        {"POST": "/api/portfolio/game_title/port_title"},
        {"DELETE": "/api/portfolio/game_title/port_title"},

        {"POST": "/api/portfolio/trade"},

        {"GET": "/api/holdings"},
        {"GET": "/api/holding/game_title/port_title/ticker"},

        {"GET": "/api/transactions"},
        {"GET": "/api/transaction/id"},
>>>>>>> fccaa93827e74133b204f7335c73749de893625a
    ]

    return Response(routes)


@api_view(['GET'])
def getPortfolios(request):
    portfolios = Portfolio.objects.all()
    serializer = PortfolioSerializer(portfolios, many=True)
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
    transaction = Transaction.objects.get(id=pk)
    serializer = TransactionSerializer(transaction, many=False)
    print(f"Successfully fetched transaction: {serializer.data}")
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
