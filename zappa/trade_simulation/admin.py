from django.contrib import admin

# Register your models here.
<<<<<<< HEAD
from .models import Holding, Portfolio, Transaction, Game
=======
from .models import Portfolio, Holding, Transaction, Game
>>>>>>> fccaa93827e74133b204f7335c73749de893625a

admin.site.register(Portfolio)
admin.site.register(Holding)
admin.site.register(Transaction)
admin.site.register(Game)
