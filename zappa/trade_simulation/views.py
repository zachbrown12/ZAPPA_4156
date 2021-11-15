from django.http import HttpResponse

# Create your views here.

<<<<<<< HEAD
def portfolios(request):
    return HttpResponse('Here are the portfolios')

def portfolio(request, pk):
    return HttpResponse('Single Portfolio' + ' ' + str(pk))
=======

def stocks(request):
    return HttpResponse("Here are the stocks")


def stock(request, pk):
    return HttpResponse("Single Stock" + " " + str(pk))
>>>>>>> fccaa93827e74133b204f7335c73749de893625a
