# views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime
import re
from funcionarios.models import funcionarios, pagamentos
from alunos.models import alunos


# PÁGINA PRINCIPAL LOGIN PARA ALUNOS
def tela_login(request):
    return render(request, "auth/login.html")


# PÁGINA DE LOGIN PARA FUNCIONARIOS
def tela_login_fun(request):
    return render(request, "auth/login_funcionarios.html")


# ROTA PARA SAIR DA CONTA
def logout(request):
    request.session.flush()
    return redirect('tela_login')


# ROTA PARA O ALUNO FAZER LOGIN
def login_aluno(request):
    if request.method != 'POST':
        return redirect('tela_login')

    try:
        cpf = re.sub(r'\D', '', request.POST.get('cpf', '').strip())
        senha = request.POST.get('senha', '').strip()

        if not cpf or not senha:
            messages.error(request, "PREENCHA OS CAMPOS ABAIXO")
            return redirect('tela_login')
        
        aluno = alunos.objects.filter(cpf=cpf).first()

        if not aluno:
            messages.error(request, "ALUNO NÃO ENCONTRADO")
            return redirect('tela_login')
        
        if not aluno.senha:
            aluno.senha = senha
            aluno.save()
            messages.success(request, "SENHA CADASTRADA COM SUCESSO. FAÇA LOGIN NOVAMENTE")
            return redirect('tela_login')
        
        pagamento = pagamentos.objects.filter(fk_aluno_id = aluno.id).last()

        if not pagamento or pagamento.data_vencimento <= datetime.today().date():
            messages.error(request,"VOCÊ PRECISA FAZER O PAGAMENTO DA MENSALIDADE")
            return redirect('tela_login')

        if senha == aluno.senha:
            request.session['id'] = aluno.id
            request.session['nome'] = aluno.nome
            return redirect('alunos:home_aluno')
        else:
            messages.error(request, "SENHA INCORRETA")
            return redirect('tela_login')
        
    except ValueError:
        return redirect('tela_login')



# ROTA PARA O FUNCIONARIO FAZER LOGIN
def login_funcionario(request):
    if request.method != 'POST':
        return redirect('tela_login_fun')

    try:
        cpf = re.sub(r'\D', '', request.POST.get('cpf', '').strip())
        senha = request.POST.get('senha', '').strip()

        if not cpf or not senha:
            messages.error(request, "PREENCHA OS CAMPOS ABAIXO")
            return redirect('tela_login_fun')
        
        funcionario = funcionarios.objects.filter(cpf=cpf).first()

        if not funcionario:
            messages.error(request, "FUNCIONÁRIO NÃO ENCONTRADO")
            return redirect('tela_login_fun')

        if not funcionario.senha:
            funcionario.senha = senha
            funcionario.save()
            messages.success(request, "SENHA CADASTRADA COM SUCESSO. FAÇA LOGIN NOVAMENTE")
            return redirect('tela_login_fun')
        
        if senha == funcionario.senha:
            request.session['id'] = funcionario.id
            request.session['nome'] = funcionario.nome
            request.session['cargo'] = funcionario.cargo

            if funcionario.cargo == "instrutor":
                return redirect('funcionarios:home_instrutor')
            elif funcionario.cargo == "administrador":
                return redirect('funcionarios:home_administrador')
            elif funcionario.cargo == "recepcionista":
                return redirect('funcionarios:home_recepcionista')
        else:
            messages.error(request, "SENHA INCORRETA")
            return redirect('tela_login_fun')
        
    except Exception:
        messages.error(request, "OCORREU UM ERRO")
        return redirect('tela_login_fun')
