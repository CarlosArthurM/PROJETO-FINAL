from django import forms
from .models import pagamentos, alunos, funcionarios
from decimal import Decimal, InvalidOperation
import re



class PessoaBaseForm(forms.ModelForm):

    def clean_nome(self):
        nome = self.cleaned_data.get('nome')

        if not nome:
            raise forms.ValidationError("PREENCHA O NOME")

        if len(nome.strip()) < 3:
            raise forms.ValidationError("NOME MUITO CURTO")

        return nome.strip()


    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')

        if cpf:
            cpf = re.sub(r'\D', '', cpf)

            if len(cpf) != 11:
                raise forms.ValidationError("CPF INVÁLIDO")

        return cpf


    def clean_telefone(self):
        telefone = self.cleaned_data.get('telefone')

        if not telefone:
            raise forms.ValidationError("PREENCHA O TELEFONE")

        telefone = re.sub(r'\D', '', telefone)

        if len(telefone) != 11:
            raise forms.ValidationError("TELEFONE INVÁLIDO")

        return telefone





class AlunoForm(PessoaBaseForm):

    def clean_data_nascimento(self):
        data_nascimento = self.cleaned_data.get('data_nascimento')

        if not data_nascimento:
            raise forms.ValidationError("PREENCHA A DATA DE NASCIMENTO")

        return data_nascimento

    class Meta:
        model = alunos
        fields = ['nome', 'cpf', 'telefone', 'sexo', 'data_nascimento']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'cpf form-control', 'placeholder': 'xxx.xxx.xxx-xx'}),
            'telefone': forms.TextInput(attrs={'class': 'tell form-control', 'placeholder': '(xx) xxxxx-xxxx'}),
            'sexo': forms.Select(attrs={'class': 'form-select'}),
            'data_nascimento': forms.DateInput(attrs={'class': 'form-control','type': 'date'})
        }





class FuncionarioForm(PessoaBaseForm):
    class Meta:
        model = funcionarios
        fields = ['nome', 'cpf', 'cargo', 'turno']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'cpf form-control'}),
            'cargo': forms.Select(attrs={'class': 'form-select'}),
            'turno': forms.Select(attrs={'class': 'form-select'})
        }
    




class PagamentoForm(forms.ModelForm):

    valor = forms.CharField(
        widget=forms.TextInput(attrs={"class": "valor form-control"})
    )
    
    def clean_valor(self):
        valor = self.cleaned_data.get('valor')
        valor = str(valor).strip().replace(".", "").replace(",", ".")

        if not valor:
            raise forms.ValidationError("INFORME UM VALOR")
        
        try:
            valor_decimal = Decimal(valor)
        except InvalidOperation:
            raise forms.ValidationError("DIGITE UM VALOR VÁLIDO")
        
        if valor_decimal <= 0:
            raise forms.ValidationError("APENAS VALORES ACIMA DE 0")
        
        return valor_decimal
    
    class Meta():
        model = pagamentos
        fields = ['forma_pagamento', 'valor']
        widgets = {
            'forma_pagamento': forms.Select(attrs={"class": "form-select"})
        }