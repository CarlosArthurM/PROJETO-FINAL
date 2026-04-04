from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from datetime import datetime, timedelta
import re
from .models import alunos, funcionarios, exercicios, fichas_treino, listas_exercicios, pagamentos
from decimal import Decimal



# ------------------- INSTRUTOR --------------------#



# PÁGINA PRINCIPAL DO INSTRUTOR
def home_instrutor(request):
    if not request.session.get("id") or request.session.get("cargo") != "instrutor":
        return redirect('tela_login_fun')
    
    nome_funcionario = request.session['nome']
    busca = request.GET.get('search')

    if busca:
        alunos_list = alunos.objects.filter(nome__icontains=busca)
    else:
        alunos_list = alunos.objects.all()

    lista_completa = []
    data_atual = datetime.today().date()

    for aluno in alunos_list:
        ficha = fichas_treino.objects.filter(fk_aluno=aluno).first()
        nascimento = aluno.data_nascimento

        idade = data_atual.year - nascimento.year
        if (data_atual.month, data_atual.day) < (nascimento.month, nascimento.day):
            idade -= 1
            
        lista_completa.append({
            "aluno": aluno,
            "idade": idade,
            "ficha": ficha
        })
    
    return render(request, "instrutor/home.html", {
        'lista_completa': lista_completa, 
        'nome_funcionario': nome_funcionario
    })






# PÁGINA PARA VISUALIZAR FICHA DE TREINO DO ALUNO
def fichas_aluno(request, aluno_id):
    if not request.session.get("id") or request.session.get("cargo") != "instrutor":
        return redirect('tela_login_fun')
    
    nome_aluno = alunos.objects.filter(id=aluno_id).first()
    
    fichas = fichas_treino.objects.filter(fk_aluno_id=aluno_id)
    exercicios_list = exercicios.objects.all().order_by('nome')

    fichas_com_exercicios = []
    for ficha in fichas:
        exercicios_lista = listas_exercicios.objects.filter(fk_ficha=ficha).select_related('fk_exercicio').values('fk_exercicio__nome','fk_exercicio__id','series','repeticoes')
        
        fichas_com_exercicios.append({
            'ficha': ficha,
            'exercicios': exercicios_lista
        })

    return render(request, "instrutor/ficha_aluno.html", {
        'fichas_com_exercicios': fichas_com_exercicios, 
        'aluno_id': aluno_id, 
        'Exercicios': exercicios_list,
        'nome_aluno': nome_aluno.nome
    })




# PÁGINA DE CADASTRO DE FICHA 
def cadastro_fichas(request, aluno_id):
    exercicios_list = exercicios.objects.all().order_by('nome')
    return render(request, 'instrutor/cadastro_fichas.html', {
        'aluno_id': aluno_id, 
        'Exercicios': exercicios_list
    })



# ROTA PARA CADASTRAR TREINO
def cadastrar_treino(request, aluno_id):
    if not request.session.get("id") or request.session.get("cargo") != "instrutor":
        return redirect('tela_login_fun')
    
    id_instrutor = request.session['id']
    
    if request.method == 'POST':
        try:
            divisao = request.POST.get('divisao')
            grupo = request.POST.get('grupo')
            nivel = request.POST.get('nivel')

            id_exercicios = request.POST.getlist("exercicio_id[]")
            lista_series = request.POST.getlist("series[]")
            lista_repeticoes = request.POST.getlist("repeticoes[]")

            if not id_exercicios or not lista_series or not lista_repeticoes:
                messages.error(request, "NÃO É POSSÍVEL CADASTRAR UMA FICHA DE TREINO SEM EXERCÍCIOS")
                return redirect('funcionarios:cadastro_fichas', aluno_id=aluno_id)

            # CRIA A FICHA
            ficha = fichas_treino.objects.create(divisao=divisao,grupo=grupo,nivel=nivel,fk_aluno_id=aluno_id,fk_funcionario_id=id_instrutor)

            # ADICIONA OS EXERCICIOS NA FICHA
            for id_ex, series, rep in zip(id_exercicios, lista_series, lista_repeticoes):
                listas_exercicios.objects.create(series=series,repeticoes=rep,fk_ficha=ficha,fk_exercicio_id=id_ex)
                
            messages.success(request, "FICHA CADASTRADA COM SUCESSO")
            return redirect('funcionarios:cadastro_fichas', aluno_id=aluno_id)
            
        except ValueError:
            messages.error(request, "OCORREU UM ERRO, VERIFIQUE OS DADOS INSERIDOS")
            return redirect('funcionarios:cadastro_fichas', aluno_id=aluno_id)
        
    return redirect('funcionarios:cadastro_fichas', aluno_id=aluno_id)




# PÁGINA ONDE SERÁ FEITO O CADASTRO DE EXERCICIOS
def cadastro_exercicios(request):
    if not request.session.get("id") or request.session.get("cargo") != "instrutor":
        return redirect('tela_login_fun')

    busca = request.GET.get('search')

    if busca:
        exercicios_list = exercicios.objects.filter(nome__icontains=busca).order_by('nome')
    else:
        exercicios_list = exercicios.objects.all().order_by('nome')

    return render(request, "instrutor/cadastro_exercicios.html", {
        'Exercicios': exercicios_list
    })




# ROTA PARA REALIZAR CADASTRO DO EXERCICIO
def cadastrar_exercicio(request):
    if not request.session.get("id") or request.session.get("cargo") != "instrutor":
        return redirect('tela_login_fun')
    

    if request.method == 'POST':
        try:
            nome_exercicio = request.POST.get('nome')
            grupo_muscular = request.POST.get('grupo_muscular')

            if not nome_exercicio:
                messages.error(request, "PREENCHA TODOS OS CAMPOS")
                return redirect('funcionarios:cadastro_exercicios')

            exercicios.objects.create(
                nome=nome_exercicio, 
                grupo_muscular=grupo_muscular
            )
            messages.success(request, "EXERCÍCIO CADASTRADO COM SUCESSO")
            return redirect('funcionarios:cadastro_exercicios')
            
        except Exception:
            messages.error(request, "OCORREU UM ERRO, VERIFIQUE OS DADOS INSERIDOS")
            return redirect('funcionarios:cadastro_exercicios')
        
    return redirect('funcionarios:cadastro_exercicios')





# ROTA PARA EDITAR O EXERCICIO 
def editar_exercicio(request, id):
    if not request.session.get("id") or request.session.get("cargo") != "instrutor":
        return redirect('tela_login_fun')
    
    if request.method == 'POST':
        try:
            novo_exercicio = request.POST.get('nome')

            if not novo_exercicio:
                messages.error(request, "PREENCHA TODOS OS CAMPOS")
                return redirect('funcionarios:cadastro_exercicios')
            
            exercicio = get_object_or_404(exercicios, id=id)
            exercicio.nome = novo_exercicio
            exercicio.grupo_muscular = request.POST.get('grupo_muscular')
            exercicio.save()
            
            messages.success(request, "EXERCÍCIO ATUALIZADO COM SUCESSO")
            return redirect('funcionarios:cadastro_exercicios')
            
        except Exception:
            messages.error(request, "OCORREU UM ERRO, VERIFIQUE OS DADOS INSERIDOS")
            return redirect('funcionarios:cadastro_exercicios')

    return redirect('funcionarios:cadastro_exercicios')





# ROTA PARA EDITAR A FICHA
def editar_ficha(request, aluno_id, treino_id):
    if not request.session.get("id") or request.session.get("cargo") != "instrutor":
        return redirect('tela_login_fun')

    if request.method == 'POST':
        try:
            grupo = request.POST.get("grupo")
            nivel = request.POST.get("nivel")

            id_exercicios = request.POST.getlist("id_exercicio[]")
            series = request.POST.getlist("series[]")
            repeticoes = request.POST.getlist("repeticoes[]")

            ficha = get_object_or_404(fichas_treino, id=treino_id)
            ficha.grupo = grupo
            ficha.nivel = nivel
            ficha.save()

            listas_exercicios.objects.filter(fk_ficha=ficha).delete()

            for id_ex, ser, rep in zip(id_exercicios, series, repeticoes):
                listas_exercicios.objects.create(
                    repeticoes=rep,
                    series=ser,
                    fk_ficha=ficha,
                    fk_exercicio_id=id_ex
                )
            
            messages.success(request, "FICHA ATUALIZADA COM SUCESSO")
            return redirect('funcionarios:fichas_aluno', aluno_id=aluno_id)
            
        except Exception as err:
            print(err)
            return redirect('funcionarios:fichas_aluno', aluno_id=aluno_id)

    return redirect('funcionarios:fichas_aluno', aluno_id=aluno_id)






# ROTA PARA ADICIONAR UM EXERCÍCIO
def adicionar_exercicio(request, aluno_id, ficha_id):
    if not request.session.get("id") or request.session.get("cargo") != "instrutor":
        return redirect('tela_login_fun')
    
    if request.method == 'POST':
        try:
            id_exercicio = request.POST.get('exercicio_id')
            series = request.POST.get('series')
            repeticoes = request.POST.get('repeticoes')

            if not id_exercicio or not series or not repeticoes:
                messages.error(request, "PREENCHA TODOS OS CAMPOS")
                return redirect('funcionarios:fichas_aluno', aluno_id=aluno_id)
            
            listas_exercicios.objects.create(
                series=series,
                repeticoes=repeticoes,
                fk_ficha_id=ficha_id,
                fk_exercicio_id=id_exercicio
            )
            messages.success(request, "EXERCÍCIO ADICIONADO COM SUCESSO")
            return redirect('funcionarios:fichas_aluno', aluno_id=aluno_id)
            
        except Exception:
            return redirect('funcionarios:fichas_aluno', aluno_id=aluno_id)

    return redirect('funcionarios:fichas_aluno', aluno_id=aluno_id)





# ROTA PARA DELETAR EXERCÍCIO 
def deletar_exercicio(request, id):
    if not request.session.get("id") or request.session.get("cargo") != "instrutor":
        return redirect('tela_login_fun')
    
    if request.method == 'GET':
        try:
            exercicios.objects.filter(id=id).delete()
            messages.success(request, "EXERCÍCIO DELETADO COM SUCESSO")
            return redirect("funcionarios:cadastro_exercicios")
            
        except:
            return redirect("funcionarios:cadastro_exercicios")
        
    return redirect("funcionarios:cadastro_exercicios")





# ROTA PARA DELETAR O TREINO DO ALUNO PELO ID
def deletar_treino(request, aluno_id):
    if not request.session.get("id") or request.session.get("cargo") != "instrutor":
        return redirect('tela_login_fun')
    
    if request.method == 'GET':
        try:
            fichas_treino.objects.filter(fk_aluno_id=aluno_id).delete()
            messages.success(request, "TREINO DELETADO COM SUCESSO")
            return redirect('funcionarios:home_instrutor')
            
        except Exception:
            return redirect('funcionarios:home_instrutor')

    return redirect('funcionarios:home_instrutor')






# ROTA PARA DELETAR A FICHA DE EXERCICIOS DO ALUNO 
def deletar_ficha(request, aluno_id, ficha_id):
    if not request.session.get("id") or request.session.get("cargo") != "instrutor":
        return redirect('tela_login_fun')
    
    if request.method == 'GET':
        try:
            listas_exercicios.objects.filter(fk_ficha_id=ficha_id).delete()
            fichas_treino.objects.filter(id=ficha_id).delete()

            messages.success(request, "FICHA DELETADA COM SUCESSO")

            fichas_total = fichas_treino.objects.filter(fk_aluno_id=aluno_id).count()
            
            if fichas_total == 0:
                return redirect('funcionarios:home_instrutor')

            return redirect('funcionarios:fichas_aluno', aluno_id=aluno_id)
            
        except Exception:
            return redirect('funcionarios:fichas_aluno', aluno_id=aluno_id)
    
    return redirect('funcionarios:fichas_aluno', aluno_id=aluno_id)













# ------------------ RECEPÇÃO -----------------#




# PÁGINA PRINCIPAL DA RECEPCIONISTA
def home_recepcionista(request):
    if not request.session.get("id") or request.session.get("cargo") != "recepcionista":
        return redirect('tela_login_fun')
    
    nome_funcionario = request.session['nome']
    busca = request.GET.get('search')

    if busca:
        alunos_list = alunos.objects.filter(nome__icontains=busca)
    else:
        alunos_list = alunos.objects.all()

    return render(request, 'recepcionista/home.html', {
        'Alunos': alunos_list, 
        'nome_funcionario': nome_funcionario
    })




# PÁGINA PARA CADASTRAR ALUNOS
def cadastro_aluno(request):
    return render(request, "recepcionista/cadastro_aluno.html")



# ROTA PARA CADASTRAR O ALUNO
def cadastrar_aluno(request):
    if not request.session.get("id") or request.session.get("cargo") != "recepcionista":
        return redirect('tela_login_fun')
    
    if request.method == 'POST':
        try:
            nome = request.POST.get('nome')
            cpf = re.sub(r'\D', '', request.POST.get('cpf', ''))
            telefone = re.sub(r'\D', '', request.POST.get('tell', ''))
            sexo = request.POST.get('sexo')
            data_nascimento = request.POST.get('data_nascimento')
            data_formatada = datetime.strptime(data_nascimento, "%Y-%m-%d").date()

            if not nome or not cpf or not telefone:
                messages.error(request, "PREENCHA TODOS OS CAMPOS")
                return redirect('funcionarios:tela_cadastro')
            
            if len(nome) < 3:
                messages.error(request, "NOME MUITO CURTO") 
                return redirect('funcionarios:tela_cadastro')
            
            if len(cpf) != 11:
                messages.error(request, "CPF INVÁLIDO")
                return redirect('funcionarios:tela_cadastro')

            if len(telefone) != 11:
                messages.error(request, "TELEFONE INVÁLIDO")
                return redirect('funcionarios:tela_cadastro')
            

            alunos.objects.create(nome=nome,cpf=cpf,sexo=sexo,data_nascimento=data_formatada, telefone=telefone)
            messages.success(request, "CADASTRADO COM SUCESSO")
            return redirect('funcionarios:tela_cadastro')
            
        except Exception:
            messages.error(request, "OCORREU UM ERRO, VERIFIQUE OS DADOS INSERIDOS")
            return redirect('funcionarios:tela_cadastro')
        
    return redirect('funcionarios:tela_cadastro')









# ROTA PARA DELETAR O ALUNO PELO ID 
def deletar_aluno(request, aluno_id):
    if not request.session.get("id") or request.session.get("cargo") != "recepcionista":
        return redirect('tela_login_fun')
    
    if request.method == 'GET':
        try:
            aluno = get_object_or_404(alunos, id=aluno_id)
            aluno.delete()
            messages.success(request, "ALUNO DELETADO COM SUCESSO")
            return redirect('funcionarios:home_recepcionista')
            
        except Exception:
            return redirect('funcionarios:home_recepcionista')
        
    return redirect('funcionarios:home_recepcionista')








# ROTA PARA ATUALIZAR INFORMAÇÕES DO ALUNO
def editar_aluno(request, aluno_id):
    if not request.session.get("id") or request.session.get("cargo") != "recepcionista":
        return redirect('tela_login_fun')

    if request.method == 'POST':
        try:
            aluno = get_object_or_404(alunos, id=aluno_id)
            novo_nome = request.POST.get('nome')
            novo_cpf = re.sub(r'\D', '', request.POST.get('cpf', ''))
            novo_telefone = re.sub(r'\D', '', request.POST.get('tell', ''))

            if not novo_nome or not novo_telefone:
                messages.error(request, "PREENCHA TODOS OS CAMPOS")
                return redirect('funcionarios:home_recepcionista')
            
            if len(novo_nome) < 3:
                messages.error(request, "NOME MUITO CURTO") 
                return redirect('funcionarios:home_recepcionista')
            
            if len(novo_cpf) != 11 and novo_cpf:
                messages.error(request, "CPF INVÁLIDO")
                return redirect('funcionarios:home_recepcionista')
            elif not novo_cpf:
                novo_cpf = aluno.cpf


            if len(novo_telefone) != 11:
                messages.error(request, "TELEFONE INVÁLIDO")
                return redirect('funcionarios:home_recepcionista')

            aluno.nome = novo_nome
            aluno.cpf = novo_cpf
            aluno.telefone = novo_telefone
            aluno.sexo = request.POST.get('sexo')
            data = request.POST.get('data_nascimento')
            aluno.data_nascimento = datetime.strptime(data, "%Y-%m-%d").date()

            aluno.save()
            messages.success(request, "DADOS DO ALUNO ATUALIZADO COM SUCESSO")
            return redirect('funcionarios:home_recepcionista')
            
        except Exception:
            messages.error(request, "OCORREU UM ERRO, VERIFIQUE OS DADOS INSERIDOS")
            return redirect('funcionarios:home_recepcionista')
        
    return redirect('funcionarios:home_recepcionista')




#página para cadastrar pagamento
def page_pagamentos(request,aluno_id):
    lista_pagamentos = pagamentos.objects.filter(fk_aluno_id=aluno_id).all()
    nome_aluno = alunos.objects.filter(id=aluno_id).first()
    
    return render(request, 'recepcionista/pagamentos.html', {
        'lista_pagamentos':lista_pagamentos, 
        'aluno_id': aluno_id, 
        'nome_aluno': nome_aluno.nome
    })




#Rota para cadastrar pagamento da mensalidade
def cadastrar_pagamento(request, aluno_id):
    if not request.session.get("id") or request.session.get("cargo") != "recepcionista":
        return redirect('tela_login_fun')
    
    if request.method == 'POST':
        try:
            forma_pagamento = request.POST.get('forma_pagamento')
            valor = request.POST.get('valor', "").strip()
            valor_decimal = Decimal(valor.replace(',','.'))

            data_vencimento = datetime.today().date() + timedelta(days=30)
            pagamentos.objects.create(forma_pagamento=forma_pagamento,valor=valor_decimal,data_vencimento=data_vencimento, fk_aluno_id=aluno_id)

            messages.success(request,"PAGAMENTO FOI CADASTRADO")
            return redirect('funcionarios:page_pagamentos', aluno_id) 
        
        except ValueError :
            messages.error(request, "DADOS INVÁLIDOS")
            return redirect('funcionarios:page_pagamentos', aluno_id) 
        except Exception:
            messages.error(request,"OCORREU UM ERRO")
            return redirect('funcionarios:page_pagamentos', aluno_id) 

        





#rota para editar o pagamento de um aluno
def editar_pagamento(request ,aluno_id ,pagamento_id):
    if not request.session.get("id") or request.session.get("cargo") != "recepcionista":
        return redirect('tela_login_fun')
    

    if request.method == 'POST':
        try:
            pagamento = get_object_or_404(pagamentos, id=pagamento_id)

            nova_forma_pagamento = request.POST.get('forma_pagamento')
            valor = request.POST.get('valor', "").strip()
            novo_valor_decimal = Decimal(valor.replace(',','.'))

            pagamento.forma_pagamento = nova_forma_pagamento
            pagamento.valor = novo_valor_decimal
            pagamento.save()

            messages.success(request,"PAGAMENTO ATUALIZADO")
            return redirect('funcionarios:page_pagamentos', aluno_id) 


        except ValueError:
            messages.error(request,"DADOS INVÁLIDOS")
            return redirect('funcionarios:page_pagamentos', aluno_id) 

        except Exception:
            messages.error(request,"OCORREU UM ERRO")
            return redirect('funcionarios:page_pagamentos', aluno_id) 
    







#rota para deletar pagamento de um aluno
def deletar_pagamento(request,aluno_id ,pagamento_id):
    if not request.session.get("id") or request.session.get("cargo") != "recepcionista":
        return redirect('tela_login_fun') 
    
    if request.method == 'GET':
        try:
            pagamentos.objects.filter(id=pagamento_id).delete()

            messages.success(request,"PAGAMENTO DELETADO")
            return redirect('funcionarios:page_pagamentos', aluno_id)    
        except Exception:
            messages.error(request,"OCORREU UM ERRO")
            return redirect('funcionarios:page_pagamentos', aluno_id)









# -------------------FUNÇÕES DO ADMINISTRADOR---------------------#



# PÁGINA PRINCIPAL ADMINISTRADOR
def home_administrador(request):
    if not request.session.get("id") or request.session.get("cargo") != "administrador":
        return redirect('tela_login_fun')
    
    nome_funcionario = request.session['nome']
    lista_funcionarios = funcionarios.objects.exclude(cargo="administrador")

    return render(request, 'adm/home.html', {'nome_funcionario': nome_funcionario, 'lista_funcionarios': lista_funcionarios})



# PÁGINA DE CADASTRO DE FUNCIONÁRIOS
def cadastro_funcionarios(request):
    return render(request, 'adm/cadastro_funcionarios.html')


# CADASTRAR FUNCIONARIO
def cadastrar_funcionario(request):
    if not request.session.get("id") or request.session.get("cargo") != "administrador":
        return redirect('tela_login_fun')
    
    if request.method == 'POST':
        try:
            nome = request.POST.get('nome')
            cpf = re.sub(r'\D', '', request.POST.get('cpf', ''))
            cargo = request.POST.get('cargo')
            turno = request.POST.get('turno')

            if not nome or not cpf:
                messages.error(request, "PREENCHA TODOS OS DADOS")
                return redirect('funcionarios:cadastro_funcionarios')
            
            if len(nome) < 3:
                messages.error(request, "NOME MUITO CURTO") 
                return redirect('funcionarios:cadastro_funcionarios')
            
            if len(cpf) != 11:
                messages.error(request, "CPF INVÁLIDO")
                return redirect('funcionarios:home_recepcionista')
                
            funcionarios.objects.create(nome=nome, cpf=cpf, cargo=cargo, turno=turno)
            messages.success(request, "FUNCIONÁRIO CADASTRADO COM SUCESSO")
            return redirect('funcionarios:cadastro_funcionarios')


        except ValueError:
            messages.error(request, "OCORREU UM ERRO, VERIFIQUE OS DADOS INSERIDOS")
            return redirect('funcionarios:cadastro_funcionarios')
        
        except Exception:
            messages.error(request, "OCORREU UM ERRO, VERIFIQUE OS DADOS INSERIDOS")
            return redirect('funcionarios:cadastro_funcionarios')
        
    return redirect('funcionarios:cadastro_funcionarios')






# ATUALIZAR INFORMAÇÕES DO FUNCIONÁRIO 
def editar_funcionario(request, funcionario_id):
    if not request.session.get("id") or request.session.get("cargo") != "administrador":
        return redirect('tela_login_fun')
    
    if request.method == 'POST':
        try:
            funcionario = get_object_or_404(funcionarios, id=funcionario_id)
            novo_nome = request.POST.get('nome')
            novo_cpf = re.sub(r'\D', '', request.POST.get('cpf', ''))

            if not novo_nome:
                messages.error(request, "PREENCHA TODOS OS CAMPOS")
                return redirect('funcionarios:home_administrador')
            
            if len(novo_nome) < 3:
                messages.error(request, "NOME MUITO CURTO") 
                return redirect('funcionarios:cadastro_funcionarios')
            
            if len(novo_cpf) != 11 and novo_cpf:
                messages.error(request, "CPF INVÁLIDO")
                return redirect('funcionarios:home_administrador')
            elif not novo_cpf:
                novo_cpf = funcionario.cpf

            funcionario.nome = novo_nome
            funcionario.cpf = novo_cpf
            funcionario.cargo = request.POST.get('cargo')
            funcionario.turno = request.POST.get('turno')
            funcionario.save()
            
            messages.success(request, "FUNCIONÁRIO ATUALIZADO COM SUCESSO")
            return redirect('funcionarios:home_administrador')
            
        except ValueError:
            messages.error(request, "OCORREU UM ERRO, VERIFIQUE OS DADOS INSERIDOS")
            return redirect('funcionarios:home_administrador')
    
    return redirect('funcionarios:home_administrador')






# DELETAR FUNCIONARIO
def deletar_funcionario(request, funcionario_id):
    if not request.session.get("id") or request.session.get("cargo") != "administrador":
        return redirect('funcionarios:tela_login_fun')
    
    if request.method == 'GET':
        try:
            funcionarios.objects.filter(id=funcionario_id).delete()
            messages.success(request, "FUNCIONÁRIO DELETADO COM SUCESSO")
            return redirect('funcionarios:home_administrador')
            
        except Exception:
            return redirect('funcionarios:home_administrador')
        
    return redirect('funcionarios:home_administrador')