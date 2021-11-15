from django.urls import path
from . import views

urlpatterns = [
<<<<<<< HEAD
    path('', views.portfolios, name="title"),
    path('portfolios/', views.portfolios, name="title"),
    path('portfolio/<str:pk>/', views.portfolios, name="title")
]
=======
    path("", views.stocks, name="tickers"),
    path("stocks/", views.stocks, name="tickers"),
    path("stock/<str:pk>/", views.stock, name="ticker"),
]
>>>>>>> fccaa93827e74133b204f7335c73749de893625a
