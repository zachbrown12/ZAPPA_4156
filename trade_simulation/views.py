from django.http import HttpResponse
from .models import Game, Portfolio
from django.shortcuts import render, redirect


def games(request):
    games = Game.objects.all()
    context = {'games': games}
    return render(request, "games.html", context)


def game(request, title):
    game = Game.objects.get(title=title)

    portfolios = Portfolio.objects.filter(game=game)

    context = {'game': game, 'portfolios': portfolios}
    return render(request, "game.html", context)
