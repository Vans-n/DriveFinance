from django.contrib import admin
from .models import Plataforma, Motorista, Corrida, Despesa, Gasto

admin.site.register(Plataforma)
admin.site.register(Motorista)
admin.site.register(Corrida)
admin.site.register(Despesa)
admin.site.register(Gasto)