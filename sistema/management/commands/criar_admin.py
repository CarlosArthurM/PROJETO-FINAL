from django.core.management.base import BaseCommand
from funcionarios.models import funcionarios
from funcionarios.forms import FuncionarioForm

class Command(BaseCommand):

    def handle(self, *args, **options):

        if funcionarios.objects.filter(cargo ="administrador").exists() == False:
            nome = input("insira o nome do admin: ").strip()
            cpf = input("insira o cpf: ")
            while True:
                print("1. Matutino")
                print("2. Vespertino")

                try:
                    op = int(input("selecione o turno em que você trabalha: "))
                    match op:
                        case 1:
                            turno = "matutino"
                            break
                        case 2:
                            turno = "vespertino"
                            break
                        case _:
                            self.stdout.write(self.style.ERROR("opção inválida, tente novamente"))

                except ValueError:
                    self.stdout.write(self.style.ERROR("digite um número válido"))

            dados = {
                "nome": nome,
                "cpf": cpf,
                "turno": turno,
                "cargo": "administrador"
            }

            form = FuncionarioForm(dados)

            if form.is_valid():
                form.save()
                self.stdout.write(self.style.SUCCESS("ADMINISTRADOR CADASTRADO COM SUCESSO"))
            else:
                for erro in form.errors.values():
                    self.stdout.write(self.style.ERROR(erro[0]))

        else:
            self.stdout.write(self.style.ERROR("ADMINISTRADOR JÁ FOI CADASTRADO"))