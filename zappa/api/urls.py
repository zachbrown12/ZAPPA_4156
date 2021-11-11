from django.urls import path
from . import views

urlpatterns = [
    path("", views.getRoutes),
    path("games/", views.getGames),
    path("games/<str:pk>", views.getGame),
    path("portfolios/", views.getPortfolios),
    path("portfolios/<str:pk>", views.getPortfolio),
    path("stocks/", views.getStocks),
    path("stocks/<str:pk>", views.getStock),
    path("transactions/", views.getTransactions),
    path("transactions/<str:pk>", views.getTransaction),
]
