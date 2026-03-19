from django.urls import path
from . import views

app_name = 'alunos'

urlpatterns = [
    path('home_aluno', views.home_aluno, name='home_aluno'),
]