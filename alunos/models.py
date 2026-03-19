from django.db import models

# Create your models here.


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
