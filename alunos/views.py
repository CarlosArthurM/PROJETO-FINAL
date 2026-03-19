from django.shortcuts import render, redirect
from funcionarios.models import fichas_treino, listas_exercicios

# PÁGINA PRINCIPAL DO ALUNO
def home_aluno(request):
    if not request.session.get("id"):
        return redirect('tela_login')
    
    aluno_id = request.session['id'] 
    lista_fichas = []

    fichas = fichas_treino.objects.filter(fk_aluno_id=aluno_id).select_related('fk_funcionario')
    for ficha in fichas:
        exercicios_ficha = listas_exercicios.objects.filter(fk_ficha=ficha).select_related('fk_exercicio')
        
        exercicios_lista = []
        for item in exercicios_ficha:
            exercicios_lista.append({
                'nome': item.fk_exercicio.nome,
                'series': item.series,
                'repeticoes': item.repeticoes
            })

        lista_fichas.append({
            "id": ficha.id,
            "divisao": ficha.divisao,
            "grupo": ficha.grupo,
            "nivel": ficha.nivel,
            "professor": ficha.fk_funcionario.nome,
            "data_criacao": ficha.data_criacao,
            "exercicios": exercicios_lista
        })


    return render(request, "alunos/home.html", {
        'fichas': lista_fichas, 
        'nome': request.session["nome"]
    })
