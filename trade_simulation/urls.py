from django.urls import path
from . import views

urlpatterns = [
    path("", views.stocks, name="tickers"),
    path("stocks/", views.stocks, name="tickers"),
    path("stock/<str:pk>/", views.stock, name="ticker"),
]
