from django.contrib import admin

# Register your models here.
from .models import Holding, Option, Portfolio, Transaction, Game

admin.site.register(Portfolio)
admin.site.register(Holding)
admin.site.register(Option)
admin.site.register(Transaction)
admin.site.register(Game)
