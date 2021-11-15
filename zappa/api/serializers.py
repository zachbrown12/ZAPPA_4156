from rest_framework import serializers
from django.contrib.auth.models import User
from trade_simulation.models import Game, Portfolio, Holding, Transaction


class UserSerializer(serializers.ModelSerializer):
    """
    User Serializer serializers all the fields in User to a useable object.
    """
    class Meta:
        model = User
        fields = "__all__"


class GameSerializer(serializers.ModelSerializer):
    """
    Game Serializer serializers all the fields in Game to a useable object.
    """
    portfolios = serializers.SerializerMethodField()

    class Meta:
        model = Game
        fields = "__all__"

    # The below code allows us to show the details of the portfolios within a game.
    def get_portfolios(self, obj):
        portfolios = obj.portfolio_set.all()
        serializer = PortfolioSerializer(portfolios, many=True)
        return serializer.data


class HoldingSerializer(serializers.ModelSerializer):
    """
    Holding Serializer serializers all the fields in Holding to a useable object.
    """
    class Meta:
        model = Holding
        fields = '__all__'


class PortfolioSerializer(serializers.ModelSerializer):
    """
    Portfolio Serializer serializers all the fields in Portfolio to a useable object.
    """
    owner = UserSerializer(many=False)
    holdings = serializers.SerializerMethodField()

    class Meta:
        model = Portfolio
        fields = "__all__"

    # The below code allows us to show the details of the holdings within a portfolio.
    def get_holdings(self, obj):
        holdings = obj.holding_set.all()
        serializer = HoldingSerializer(holdings, many=True)
        return serializer.data


class TransactionSerializer(serializers.ModelSerializer):
    """
    Transaction Serializer serializers all the fields in Transaction to a useable object.
    """
    class Meta:
        model = Transaction
        fields = "__all__"
