from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def stocks(request):
    return HttpResponse('Here are the stocks')

def stock(request, pk):
    return HttpResponse('Single Stock' + ' ' + str(pk))