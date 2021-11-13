from rest_framework import serializers
from django.contrib.auth.models import User
from trade_simulation.models import Game, Portfolio, Holding, Transaction


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class GameSerializer(serializers.ModelSerializer):
    portfolios = serializers.SerializerMethodField()

    class Meta:
        model = Game
        fields = "__all__"

    def get_portfolios(self, obj):
        portfolios = obj.portfolio_set.all()
        for portfolio in portfolios:
            portfolio.computeTotalValue()
        serializer = PortfolioSerializer(portfolios, many=True)
        return serializer.data


class HoldingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Holding
        fields = '__all__'


class PortfolioSerializer(serializers.ModelSerializer):
    owner = UserSerializer(many=False)
    holdings = serializers.SerializerMethodField()

    class Meta:
        model = Portfolio
        fields = "__all__"

    def get_holdings(self, obj):
        holdings = obj.holding_set.all()
        serializer = HoldingSerializer(holdings, many=True)
        return serializer.data


class TransactionSerializer(serializers.ModelSerializer):
    portfolio = PortfolioSerializer(many=False)
    holding = HoldingSerializer(many=False)

    class Meta:
        model = Transaction
        fields = "__all__"
