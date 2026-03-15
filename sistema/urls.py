# urls.py
from django.urls import path
from . import views

urlpatterns = [
    # páginas principais
    path('', views.tela_login, name='tela_login'),
    path('login_funcionarios', views.tela_login_fun, name='tela_login_fun'),

    #ROTA PARA DESLOGAR
    path('logout', views.logout, name='logout'),

    #página cadastro de alunos 
    path('cadastro_aluno', views.cadastro_aluno, name='tela_cadastro'),

    #página cadastro de funcionários
    path('cadastro_funcionarios', views.cadastro_funcionarios, name='cadastro_funcionarios'),
    
    # Home pages
    path('home_recepcionista', views.home_recepcionista, name='home_recepcionista'),
    path('home_administrador', views.home_administrador, name='home_administrador'),
    path('home_aluno', views.home_aluno, name='home_aluno'),
    path('home_instrutor', views.home_instrutor, name='home_instrutor'),
    
    # Login
    path('login_aluno', views.login_aluno, name='login_aluno'),
    path('login_funcionario', views.login_funcionario, name='login_funcionario'),
    
    # Funcionalidades do Instrutor
    path('cadastro_fichas/<int:aluno_id>', views.cadastro_fichas, name='cadastro_fichas'),
    path('fichas_aluno/<int:aluno_id>', views.fichas_aluno, name='fichas_aluno'),
    path('cadastrar_treino/<int:aluno_id>', views.cadastrar_treino, name='cadastrar_treino'),
    path('cadastro_exercicios', views.cadastro_exercicios, name='cadastro_exercicios'),
    path('cadastrar_exercicio', views.cadastrar_exercicio, name='cadastrar_exercicio'),
    path('editar_exercicio/<int:id>', views.editar_exercicio, name='editar_exercicio'),
    path('editar_ficha/<int:aluno_id>/<int:treino_id>', views.editar_ficha, name='editar_ficha'),
    path('adicionar_exercicio/<int:aluno_id>/<int:ficha_id>', views.adicionar_exercicio, name='adicionar_exercicio'),
    path('deletar_exercicio/<int:id>', views.deletar_exercicio, name='deletar_exercicio'),
    path('deletar_treino/<int:aluno_id>', views.deletar_treino, name='deletar_treino'),
    path('deletar_ficha/<int:aluno_id>/<int:ficha_id>', views.deletar_ficha, name='deletar_ficha'),
    
    # Funcionalidades da Recepção
    path('cadastrar_aluno', views.cadastrar_aluno, name='cadastrar_aluno'),
    path('deletar_aluno/<int:aluno_id>', views.deletar_aluno, name='deletar_aluno'),
    path('editar_aluno/<int:aluno_id>', views.editar_aluno, name='editar_aluno'),
    
    # Funcionalidades do Administrador
    path('cadastrar_funcionario', views.cadastrar_funcionario, name='cadastrar_funcionario'),
    path('editar_funcionario/<int:funcionario_id>', views.editar_funcionario, name='editar_funcionario'),
    path('deletar_funcionario/<int:funcionario_id>', views.deletar_funcionario, name='deletar_funcionario'),
]