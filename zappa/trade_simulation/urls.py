from django.urls import path, include
from . import views 

urlpatterns = [
    path('', views.stocks, name="tickers"),
    path('stocks/', views.stocks, name="tickers"),
    path('stock/<str:pk>/', views.stock, name="ticker")
]