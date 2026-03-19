# urls.py
from django.urls import path
from . import views

urlpatterns = [
    # páginas principais
    path('', views.tela_login, name='tela_login'),
    path('login_funcionarios', views.tela_login_fun, name='tela_login_fun'),

    #ROTA PARA DESLOGAR
    path('logout', views.logout, name='logout'),
    
    # Login
    path('login_aluno', views.login_aluno, name='login_aluno'),
    path('login_funcionario', views.login_funcionario, name='login_funcionario'),
]