from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def portfolios(request):
    return HttpResponse('Here are the portfolios')

def portfolio(request, pk):
    return HttpResponse('Single Portfolio' + ' ' + str(pk))