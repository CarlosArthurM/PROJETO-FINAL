# 🏋️ Sistema de Gerenciamento de Academia

Sistema web desenvolvido para facilitar o gerenciamento de academias, permitindo o controle de alunos, funcionários e operações do dia a dia de forma simples e eficiente.

---

## 🚀 Tecnologias utilizadas

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=fff)
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=fff)
![Bootstrap](https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=fff)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=fff)

---

## 📋 Funcionalidades

### 👨‍💼 Administrador
- Gerenciamento de funcionários (instrutores e recepcionistas)
- Cadastro, edição e exclusão de funcionários

### 🏋️ Instrutor
- Gerenciamento de fichas de treino
- Cadastro, edição e exclusão de exercícios

### 🧾 Recepcionista
- Gerenciamento de alunos
- Cadastro, edição e exclusão de alunos
- Controle de pagamentos

---

## ⚙️ Como executar o projeto

### 1. Clone o repositório
```bash
git clone https://github.com/CarlosArthurM/PROJETO-FINAL
```

### 2. Acesse a pasta do projeto
```bash
cd PROJETO-FINAL
```

### 3. Crie um ambiente virtual
```bash
python -m venv venv
```

### 4. Ative o ambiente virtual

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 5. Instale as dependências
```bash
pip install -r requisitos.txt
```

### 6. Execute os comandos iniciais
```bash
python manage.py criar_exercicios
python manage.py criar_admin
```

---

## 🧪 Exemplo de criação de administrador

```
insira o nome do admin: Carlos Arthur
insira o cpf: 12345678901

1. Matutino
2. Vespertino

selecione o turno em que você trabalha: 1

ADMINISTRADOR CADASTRADO COM SUCESSO
```

---

## 💡 Possíveis melhorias futuras

- Sistema de autenticação com login
- Dashboard com gráficos
- Integração com pagamentos online
- Deploy em produção

---

## 📌 Observações

Este projeto foi desenvolvido com fins educacionais e prática de desenvolvimento web com Django.
