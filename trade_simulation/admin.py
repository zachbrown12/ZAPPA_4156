from django.contrib import admin

# Register your models here.
from .models import Holding, Portfolio, Transaction, Game

admin.site.register(Portfolio)
admin.site.register(Holding)
admin.site.register(Transaction)
admin.site.register(Game)
