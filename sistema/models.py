from django.db import models


# tabela alunos
class alunos(models.Model):

    SEXO_CHOICES = [
        ('F', 'F'),
        ('M', 'M')
    ]

    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=200)
    cpf = models.CharField(max_length=20, unique=True)
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)
    senha = models.CharField(max_length=200, null=True, blank=True)
    data_nascimento = models.DateField()
    telefone = models.CharField(max_length=20, unique=True)
    data_matricula = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "alunos"


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
    nome = models.CharField(max_length=200)
    cargo = models.CharField(max_length=20, choices=CARGO_CHOICES)
    cpf = models.CharField(max_length=20, unique=True)
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
    nome = models.CharField(max_length=200)
    grupo_muscular = models.CharField(max_length=100, choices=GRUPO_MUSCULAR_CHOICES)

    class Meta:
        db_table = "exercicios"


# tabela lista_exercicios
class lista_exercicios(models.Model):

    id = models.AutoField(primary_key=True)
    repeticoes = models.IntegerField()
    series = models.IntegerField()

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
        db_table = "lista_exercicios"