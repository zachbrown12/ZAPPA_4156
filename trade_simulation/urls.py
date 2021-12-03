from django.urls import path
from . import views

urlpatterns = [
    path("", views.games, name="games"),
    path("games", views.games, name="games"),
    path('game/<str:title>/', views.game, name="game"),
]
