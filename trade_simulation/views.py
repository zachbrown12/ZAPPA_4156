from django.http import HttpResponse
from .models import Game, Portfolio, Holding
from django.shortcuts import render, redirect


def games(request):
    games = Game.objects.all()
    context = {'games': games}

    return render(request, "games.html", context)


def game(request, pk):
    game = Game.objects.get(uid=pk)
    portfolios = Portfolio.objects.filter(game=game)

    context = {'game': game, 'portfolios': portfolios}
    return render(request, "game.html", context)


def portfolio(request, pk):
    portfolio = Portfolio.objects.get(uid=pk)
    holdings = Holding.objects.filter(portfolio=portfolio)

    context = {'portfolio': portfolio, 'holdings': holdings}
    return render(request, "portfolio.html", context)
