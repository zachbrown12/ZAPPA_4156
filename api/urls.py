from django.urls import path
from . import views

urlpatterns = [
    path("", views.get_routes),
    path("games/", views.handle_games),
    path("game/<str:game_title>", views.handle_game),
    path("portfolios", views.handle_portfolios),
    path("portfolio/<str:game_title>/<str:port_title>/", views.handle_portfolio),
    path("portfolio/trade", views.trade),
    path("holdings/", views.handle_holdings),
    path("holding/<str:port_title>/<str:game_title>/<str:ticker>", views.handle_holding),
    path("options/", views.handle_options),
    path("option/<str:port_title>/<str:game_title>/<str:contract>", views.handle_option),
    path("transactions/", views.handle_transactions),
    path("transaction/<str:pk>", views.handle_transaction)
]
