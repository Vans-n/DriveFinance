from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('cadastro/', views.cadastro_view, name='cadastro'),
    path('', views.home, name='home'),

    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # Corridas
    path('corridas/', views.listar_corridas, name='lista_corridas'),
    path('corridas/nova/', views.criar_corrida, name='nova_corrida'),
    path('corridas/editar/<int:id>/', views.editar_corrida, name='editar_corrida'),
    path('corridas/excluir/<int:id>/', views.excluir_corrida, name='excluir_corrida'),
    path('plataformas/nova/', views.criar_plataforma, name='nova_plataforma'),

    # Despesas
    path('despesas/', views.listar_despesas, name='lista_despesas'),
    path('despesas/nova/', views.criar_despesa, name='nova_despesa'),
    path('despesas/editar/<int:id>/', views.editar_despesa, name='editar_despesa'),
    path('despesas/excluir/<int:id>/', views.excluir_despesa, name='excluir_despesa'),
]