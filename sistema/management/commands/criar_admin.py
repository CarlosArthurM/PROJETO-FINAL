from django.core.management.base import BaseCommand
from sistema.models import funcionarios

class Command(BaseCommand):

    def handle(self, *args, **options):

        if funcionarios.objects.filter(cargo ="administrador").exists() == False:
            funcionarios.objects.create(nome="João Pedro Mello",cargo="administrador",cpf="98763095893",turno="matutino")

            self.stdout.write(self.style.SUCCESS("ADMINISTRADOR CADASTRADO COM SUCESSO"))

        else:
            self.stdout.write(self.style.ERROR("ADMINISTRADOR JÁ FOI CADASTRADO"))