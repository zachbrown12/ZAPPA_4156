from django.urls import path, include
from . import views 

urlpatterns = [
    path('', views.portfolios, name="title"),
    path('portfolios/', views.portfolios, name="title"),
    path('portfolio/<str:pk>/', views.portfolios, name="title")
]