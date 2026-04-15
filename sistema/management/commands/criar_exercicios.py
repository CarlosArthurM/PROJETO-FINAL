from django.core.management.base import BaseCommand
from funcionarios.models import exercicios

class Command(BaseCommand):

    def handle(self, *args, **options):
        
        if exercicios.objects.exists() == False:


            lista_exercicios = {
                'Membros Superiores' : ['Supino Reto','Supino Inclinado','Crossover','Elevação Lateral','Rosca Direta','Rosca Martelo','Remada Alta','Rosca Scott','Triceps Pulley','Triceps Francês','Remada Curvada','Remada Baixa','Puxador Frontal'],
                'Músculos do Tórax e Abdômen' : ['Abdominal Reto', 'Prancha', 'Abdominal na Polia', 'Abdominal Cruzado', 'Roda Abdominal'],
                'Membros Inferiores': ['Agachamento Sumô', 'Agachamento Smith', 'Stiff', 'Leg Press', 'Agachamento Búlgaro', 'Mesa Flexora', 'Afundo', 'Agachamento Hack', 'Levantamento Terra']
            }

            for grupo, lista in lista_exercicios.items():
                for nome in lista:
                    exercicios.objects.get_or_create(nome=nome, grupo_muscular=grupo)

            
            self.stdout.write(self.style.SUCCESS('EXERCÍCIOS CADASTRADOS COM SUCESSO'))

        
        else:
            self.stdout.write(self.style.ERROR('O BANCO JÁ TEM EXERCÍCIOS CADASTRADOS'))