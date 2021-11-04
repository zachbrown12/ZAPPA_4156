from rest_framework import serializers
from django.contrib.auth.models import User
from trade_simulation.models import Game, Portfolio, Stock, Transaction


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields ='__all__'

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'

class PortfolioSerializer(serializers.ModelSerializer):
    owner = UserSerializer(many=False)
    game = GameSerializer(many=False)
    class Meta:
        model = Portfolio
        fields = '__all__'

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    portfolio = PortfolioSerializer(many=False)
    stock = StockSerializer(many=False)
    class Meta:
        model = Transaction
        fields = '__all__'


