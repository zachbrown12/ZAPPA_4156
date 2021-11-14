from django.urls import path
from . import views

urlpatterns = [
    path("", views.getRoutes),
    path("games/", views.handle_games),
    path("portfolios/", views.handle_portfolios),
    path("portfolio/<str:pk>", views.handle_portfolio_pk),
    path("portfolio/<str:pk>/trade", views.trade),
    path("holdings/", views.handle_holdings),
    path("holding/<str:pk>", views.handle_holding),
    path("transactions/", views.handle_transactions),
    path("transaction/<str:pk>", views.handle_transaction),
]
