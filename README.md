#  Drive Finance

### Controle seus ganhos em tempo real 

Organize corridas, registre despesas e visualize seu lucro de forma clara e inteligente tudo em um só lugar, com rapidez e simplicidade.

---

## 📌 Sobre o projeto

O **Drive Finance** é um sistema web desenvolvido com Django para ajudar no controle financeiro pessoal, especialmente para quem trabalha com ganhos variáveis (como motoristas de aplicativos).

A proposta é simples: transformar dados financeiros em informações claras para tomada de decisão.

---

## ⚙️ Funcionalidades
```
✔️ Cadastro de rendas (corridas / ganhos)
✔️ Registro de gastos
✔️ Controle de reserva financeira
✔️ Dashboard com saldo automático
✔️ Interface simples e intuitiva
✔️ Sistema de autenticação de usuários
```

---

## 📊 Como funciona

O sistema realiza o cálculo automaticamente:

**Saldo = Renda - Gastos**

A **reserva financeira** é exibida separadamente, permitindo um controle mais estratégico do dinheiro.

---

## 🛠️ Tecnologias utilizadas

* Python
* Django
* HTML5
* CSS3
* SQLite

---

## 🚀 Como executar o projeto

```bash
# Clone o repositório
git clone https://github.com/Vans-n/DriveFinance.git

# Acesse a pasta
cd DriveFinance

# Crie o ambiente virtual
python -m venv venv

# Ative o ambiente
venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt

# Execute as migrações
python manage.py migrate

# Inicie o servidor
python manage.py runserver
```

---

## 🔐 Acesso ao sistema

Você pode acessar o sistema de duas formas:

### 👤 Usuário comum

Realize o cadastro diretamente pela interface da aplicação.

### 🛠️ Administrador (opcional)

Para acessar o painel administrativo do Django (`/admin`), crie um superusuário:

```bash
python manage.py createsuperuser
```

---

## 📷 Preview

<img width="1394" height="626" alt="image" src="https://github.com/user-attachments/assets/a7a337e7-356f-4316-b10a-eb2daff351ba" />


---

## 📚 Aprendizados

Este projeto foi desenvolvido com foco em:

* Desenvolvimento web com Django
* Estruturação de sistemas CRUD
* Organização de código
* Versionamento com Git e GitHub

---

## 📄 Licença

Este projeto tem finalidade educacional.
