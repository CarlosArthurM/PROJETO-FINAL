from django.db import models
from alunos.models import alunos


#tabela pagamentos
class pagamentos(models.Model):

    PAGAMENTO_CHOICES = [
        ('Cartão Crédito','Cartão Crédito'),
        ('Cartão Débito','Cartão Débito'),
        ('Pix','Pix'),
        ('Dinheiro','Dinheiro')
    ]

    id = models.AutoField(primary_key=True)
    forma_pagamento = models.CharField(max_length=20, choices=PAGAMENTO_CHOICES, null=False)
    valor = models.DecimalField(decimal_places=2, max_digits=10, null=False)
    data_pagamento = models.DateField(auto_now_add=True)
    data_vencimento = models.DateField(null=False)
    fk_aluno = models.ForeignKey(alunos,db_column='fk_aluno', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = "pagamentos"




# tabela funcionarios
class funcionarios(models.Model):

    CARGO_CHOICES = [
        ('instrutor','instrutor'),
        ('recepcionista','recepcionista'),
        ('administrador','administrador')
    ]

    TURNO_CHOICES = [
        ('matutino','matutino'),
        ('vespertino','vespertino')
    ]

    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=200, null=False)
    cargo = models.CharField(max_length=20, choices=CARGO_CHOICES, null=False)
    cpf = models.CharField(max_length=20, unique=True, null=False)
    senha = models.CharField(max_length=200, null=True, blank=True)
    turno = models.CharField(max_length=20, choices=TURNO_CHOICES)

    class Meta:
        db_table = "funcionarios"




# tabela fichas de treino
class fichas_treino(models.Model):

    DIVISAO_CHOICES = [
        ('ABC','ABC'),
        ('ABCD','ABCD'),
        ('ABCDE','ABCDE'),
        ('FULL BODY','FULL BODY')
    ]

    GRUPO_CHOICES = [
        ('A','A'),
        ('B','B'),
        ('C','C'),
        ('D','D'),
        ('E','E'),
        ('FULL BODY','FULL BODY')
    ]

    NIVEL_CHOICES = [
        ('Iniciante','Iniciante'),
        ('Intermediário','Intermediário'),
        ('Avançado','Avançado'),
        ('Personalizado','Personalizado')
    ]

    id = models.AutoField(primary_key=True)
    divisao = models.CharField(max_length=20, choices=DIVISAO_CHOICES)
    grupo = models.CharField(max_length=20, choices=GRUPO_CHOICES, null=True, blank=True)
    nivel = models.CharField(max_length=20, choices=NIVEL_CHOICES)
    data_criacao = models.DateTimeField(auto_now_add=True)

    fk_aluno = models.ForeignKey(
        alunos,
        on_delete=models.CASCADE,
        db_column="fk_aluno"
    )

    fk_funcionario = models.ForeignKey(
        funcionarios,
        on_delete=models.CASCADE,
        db_column="fk_funcionario"
    )

    class Meta:
        db_table = "fichas_treino"





# tabela exercicios
class exercicios(models.Model):

    GRUPO_MUSCULAR_CHOICES = [
        ('Membros Superiores','Membros Superiores'),
        ('Músculos do Tórax e Abdômen','Músculos do Tórax e Abdômen'),
        ('Membros Inferiores','Membros Inferiores')
    ]

    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=200, null=False)
    grupo_muscular = models.CharField(max_length=100, choices=GRUPO_MUSCULAR_CHOICES)

    class Meta:
        db_table = "exercicios"






# tabela lista_exercicios
class listas_exercicios(models.Model):

    id = models.AutoField(primary_key=True)
    repeticoes = models.IntegerField(null=False)
    series = models.IntegerField(null=False)

    fk_ficha = models.ForeignKey(
        fichas_treino,
        on_delete=models.CASCADE,
        db_column="fk_ficha"
    )

    fk_exercicio = models.ForeignKey(
        exercicios,
        on_delete=models.CASCADE,
        db_column="fk_exercicio"
    )

    class Meta:
        db_table = "listas_exercicios"