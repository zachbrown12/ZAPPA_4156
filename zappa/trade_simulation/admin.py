from django.contrib import admin

# Register your models here.
from .models import Portfolio, Stock, Transaction, Game

admin.site.register(Portfolio)
admin.site.register(Stock)
admin.site.register(Transaction)
admin.site.register(Game)
