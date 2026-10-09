# Sistema CRUD em Python com Flask

## 📋 Descrição do Sistema
Este projeto consiste em uma aplicação web de **CRUD (Create, Read, Update, Delete)** desenvolvida em **Python** utilizando o microframework **Flask**. A aplicação foi estruturada para gerenciar registros de forma eficiente, integrando um banco de dados relacional via ORM e oferecendo uma interface limpa e responsiva.

---

## 🛠️ O que foi usado (Tecnologias e Dependências)
- **Python** — Linguagem principal de programação.
- **Flask** — Microframework web utilizado para gerenciar rotas e requisições HTTP.
- **Flask-SQLAlchemy** — Extensão ORM para mapeamento objeto-relacional e interação com o banco de dados.
- **Flask-Bootstrap5** — Integração do framework CSS Bootstrap 5 para estilização e componentes visuais.
- **Jinja2** — Motor de templates HTML do Flask.
- **Click** — Biblioteca utilizada pelo Flask para gerenciamento de comandos via CLI.
- **Itsdangerous** — Utilitário para assinatura de dados e segurança de tokens.
- **Blinker** — Sistema de gerenciamento de sinais e eventos.

---

## ⚙️ Requerimentos
Certifique-se de ter os seguintes itens instalados em sua máquina:
- **Python** (versão 3.10 ou superior recomendada)
- **Git** (opcional, para clonar o repositório)

---

## 📥 Como Instalar

1. **Clone ou baixe o repositório do projeto:**
   ```bash
   git clone https://github.com/Danylohcs/Flask-CRUD.git
   cd "CRUD Python"
   ```

2. **Crie e ative um ambiente virtual (Recomendado):**
   - **No Windows (CMD / PowerShell):**
     ```bash
     python -m venv .venv
     .venv\Scripts\activate
     ```
   - **No Linux / macOS:**
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```

3. **Instale as dependências:**
   Caso o ambiente virtual já possua os pacotes ou precise instalar as bibliotecas principais do projeto, execute:
   ```bash
   pip install flask flask-sqlalchemy flask-bootstrap5
   ```

---

## 🚀 Como Rodar

1. **Configure a aplicação Flask:**
   Defina a variável de ambiente principal do projeto (substitua `app.py` pelo nome do arquivo principal de inicialização, caso seja diferente):
   - **No Windows (CMD):**
     ```cmd
     set FLASK_APP=app.py
     set FLASK_DEBUG=1
     ```
   - **No Windows (PowerShell):**
     ```powershell
     $env:FLASK_APP="app.py"
     $env:FLASK_DEBUG="1"
     ```
   - **No Linux / macOS:**
     ```bash
     export FLASK_APP=app.py
     export FLASK_DEBUG=1
     ```

2. **Execute o servidor de desenvolvimento:**
   ```bash
   flask run
   ```
   *Alternativamente, você pode executar diretamente via Python:*
   ```bash
   python app.py
   ```

3. **Acesse no navegador:**
   Abra o seu navegador de preferência e acesse o link gerado (geralmente):
   ```text
   http://127.0.0.1:5000
   ```