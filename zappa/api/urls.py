from django.urls import path
from .import views

urlpatterns = [
    path('', views.getRoutes),
    path('games/', views.getGames),
    path('games/<str:pk>', views.getGame),
    path('portfolios/', views.getPortfolios),
    path('portfolios/<str:pk>', views.getPortfolio),
    path('newportfolio/', views.makePortfolio),
    path('buystock/<str:pk>', views.buyStock),
    path('sellstock/<str:pk>', views.sellStock),
    path('holdings/', views.getHoldings),
    path('holding/<str:pk>', views.getHolding),
    path('transactions/', views.getTransactions),
    path('transactions/<str:pk>', views.getTransaction),
]