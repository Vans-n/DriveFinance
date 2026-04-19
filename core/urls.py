from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # Corridas
    path('corridas/', views.listar_corridas, name='listar_corridas'),
    path('corridas/nova/', views.criar_corrida, name='criar_corrida'),
    path('corridas/editar/<int:id>/', views.editar_corrida, name='editar_corrida'),
    path('corridas/excluir/<int:id>/', views.excluir_corrida, name='excluir_corrida'),

    # DESPESAS
    path('despesas/', views.listar_despesas, name='listar_despesas'),
    path('despesas/nova/', views.criar_despesa, name='criar_despesa'),
    path('despesas/editar/<int:id>/', views.editar_despesa, name='editar_despesa'),
    path('despesas/excluir/<int:id>/', views.excluir_despesa, name='excluir_despesa'),
]