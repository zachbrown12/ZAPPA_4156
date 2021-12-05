from django.urls import path
from . import views

urlpatterns = [
    path("", views.games, name="games"),
    path("games", views.games, name="games"),
    path('game/<str:pk>/', views.game, name="game"),
    path('portfolio/<str:pk>/', views.portfolio, name="portfolio"),
]
