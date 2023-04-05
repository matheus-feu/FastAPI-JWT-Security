[![wakatime](https://wakatime.com/badge/user/3bd24664-869f-460a-94e1-b98da8136504/project/84b221e2-7b66-4ea3-b381-f11d8513afe0.svg)](https://wakatime.com/badge/user/3bd24664-869f-460a-94e1-b98da8136504/project/84b221e2-7b66-4ea3-b381-f11d8513afe0)

<h2 align="center">  FastAPI-JWT-Security 🚀 </h2>

<p align="center">  Uma segurança JWT simples e fácil de usar para FastAPI. </p>

## 📝 Índice

- [Sobre](#sobre)
- [Tecnologias utilizadas](#tecnologias-utilizadas)
- [Executando o projeto](#executando-o-projeto)
- [Endpoints](#endpoints)
- [Bibliotecas utilizadas](#bibliotecas-utilizadas)
- [Contato](#contato)

## 📖 Sobre

Através da API é possível realizar o CRUD dos usuários e artigos.
Nela o usuário precisa se cadastrar, se autenticar, verificar o status da autenticação e realizar o login para obter o
token de acesso. Com o token de acesso é possível realizar as operações da API.

A API utiliza-se do SQLAlchemy para realizar as operações no banco de dados PostgreSQL, e do PyJWT para gerar o token de
acesso. O banco de dados é executado em um container Docker.

Oferece uma série de recursos para a segurança da API, como: Autenticação JWT, Autorização JWT, Criptografia de senha,
Validação de senha, Validação de e-mail, Validação de CPF e Validação de data de nascimento.

## 🔗 Tecnologias utilizadas

![Python](https://img.shields.io/badge/-Python-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/-FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-336791?style=flat-square&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/-Docker-2496ED?style=flat-square&logo=docker&logoColor=white)
![PyCharm](https://img.shields.io/badge/-PyCharm-000000?style=flat-square&logo=pycharm&logoColor=white)
![Git](https://img.shields.io/badge/-Git-F05032?style=flat-square&logo=git&logoColor=white)
![GitHub](https://img.shields.io/badge/-GitHub-181717?style=flat-square&logo=github&logoColor=white)

## ⚙️ Executando o projeto

#### 💻 Pré-requisitos

Antes de começar, você vai precisar ter instalado em sua máquina as seguintes ferramentas:

- Você precisa instalar o [Docker](https://docs.docker.com/engine/install/) para executar o banco de dados PostgreSQL.
- Instalar a versão 3.11 do [Python](https://www.python.org/downloads/).
- Possuir um editor para trabalhar com o código como [VSCode](https://code.visualstudio.com/)
  ou [PyCharm](https://www.jetbrains.com/pt-br/pycharm/).
- Ter o [Git](https://git-scm.com/) instalado para clonar o projeto.

Com tudo devidamente instalado, vamos ao passo a passo de como executar o projeto.

#### 📁 Clonar o repositório

```bash
# Clone este repositório
git clone https://github.com/matheus-feu/FastAPI-JWT-Security.git

# Entrar no diretório
cd FastAPI-JWT-Security
````

#### 🐳 Docker

```bash
# Execute o comando para criar o container do banco de dados
docker-compose up -d
```

#### 🐍 Python

```bash
# Criar um ambiente virtual
python -m venv venv

# Ativar o ambiente virtual
venv\Scripts\activate

# Instalar as dependências
pip install -r requirements.txt

# Criar as tabelas no banco de dados
python create_tables.py

# Executar o projeto
uvicorn main:app --reload
```

## 📌 Endpoints

Ao concluir todas as etapas anteriores, você terá a API rodando em sua máquina. Para acessar a documentação da API,
acesse o endereço http://localhost:8000/docs ou modo interativo http://localhost:8000/redoc.

![documentacao](https://imgur.com/wFAXU8E.png)

O funcionamento da API é simples, primeiro é necessário realizar o cadastro do usuário, depois realizar o login para
obter o token de acesso, e com o token de acesso é possível realizar as operações da API.

#### 📝 Usuários

O fluxo de funcionamento ocorre da seguinte forma:

- Cadastro do usuário na rota **/api/v1/usuarios/signup**, siga o exemplo abaixo:

Nesta rota é necessário informar o nome completo, e-mail, telefone, CPF, data de nascimento, selecionar se é admin ou
não e a senha. Após o cadastro, o usuário receberá um e-mail de confirmação de cadastro,
este e-mail precisa ser configurado no arquivo **.env**, substituindo o e-mail e senha do remetente e o e-mail do
destinatário.

```bash
    {
        "name_complete":"John Doe",
        "date_of_birth":"2023-04-03",
        "email":"johndoe@email.com",
        "telephone":"52962524873",
        "cpf":"40366865511",
        "is_admin":"true",
        "password":"teste123"
    }
```

Saída:

```bash
{
    "name_complete": "John doe",
    "date_of_birth": "2023-04-03",
    "email": "johndoe@email.com",
    "telephone": "52962524873",
    "cpf": "40366865511",
    "is_admin": true,
    "id": 1,
    "created_at": "2023-04-05T01:50:35.257576",
    "updated_at": "2023-04-05T01:50:35.257576",
    "send_email": "Olá seu cadastro foi realizado com sucesso, enviaremos um e-mail de confirmação"
}
```

- Após o cadastro, o usuário receberá um e-mail de confirmação de cadastro, este e-mail precisa ser configurado no
  arquivo **.env**, substituindo o e-mail e senha do remetente e o e-mail do destinatário.

![email](https://imgur.com/pDQ3BM1.png)

- Na rota **/api/v1/usuarios/me** é possível visualizar os dados do usuário logado, retornando as informações.


- É possível pegar todos os usuários cadastrados na rota **/api/v1/usuarios/**, neste exemplo há apenas um usuário.


- Da mesma forma a API permite buscar um usuário específico na rota **/api/v1/usuarios/{id}**, pelo respectivo ID e nela
  consta a lista de artigos que aquele usuário criou.

Exemplo:

```bash
{
    "name_complete": "John doe",
    "date_of_birth": "2023-04-03",
    "email": "johndoe@email.com",
    "telephone": "52962524873",
    "cpf": "40366865511",
    "is_admin": true,
    "articles": [
        {
            "title": "Segundo Artigo de Teste",
            "description": "Somente um artigo para testar",
            "url_font": "http://www.chegouemail.com.br/news/L1-88-2-H.html"
        },
        {
            "title": "Primeiro Artigo de Teste",
            "description": "Somente um artigo para testar",
            "url_font": "http://www.chegouemail.com.br/news/L1-88-2-H.html"
        }
    ]
}
```

- Também é possivel atualizar os dados do usuário na rota **/api/v1/usuarios/{id}**, basta informar o ID do usuário e as
  informações que deseja atualizar.


- Na rota **/api/v1/usuarios/{id}** é possível deletar um usuário, basta informar o ID do usuário que deseja deletar.

### 📝 Autenticação

- Login na rota **/api/v1/usuarios/login**:

Nesta rota é necessário informar o e-mail e a senha do usuário cadastrado. Após o login, irá gerar um token JWT de
acesso, permitindo que novas requisições sejam feitas.

Na documentação da API clique em Authorize e informe o login e senha do usuário cadastrado, após isso clique em
Authorize, dessa forma
o token de acesso será gerado e será possível realizar as operações da API.

![login](https://imgur.com/0RQCwXC.png)

### 📝 Status

- Status da autenticação na rota **/api/v1/status/status** retorna o status da aplicação.

Corpo de resposta:

```bash
{
  "sucess": true,
  "version": "1.0.0",
  "user": "johndoe@email.com",
  "status": "API is running",
  "message": "Welcome to the API"
}
```

### 📝 Artigos

Não muito diferente do fluxo de funcionamento dos usuários, o fluxo de funcionamento dos artigos ocorre da seguinte
forma:

- Criação de artigo na rota **/api/v1/artigos/**, siga o exemplo abaixo:

Nesta rota é necessário informar o título, descrição e a url da fonte do artigo. Após a criação, o artigo será
listado na rota **/api/v1/artigos/**.

```bash
{
    "title":"Primeiro Artigo de Teste",
    "description":"Somente um artigo para testar",
    "url_font":"http://www.chegouemail.com.br/news/L1-88-2-H.html"
}
```

- É possível pegar todos os artigos cadastrados na rota **/api/v1/artigos/**.

```bash
[
  {
    "title": "Segundo Artigo de Teste",
    "description": "Somente um artigo para testar",
    "url_font": "http://www.chegouemail.com.br/news/L1-88-2-H.html",
    "id": 1,
    "user_id": 1,
    "created_at": "2023-04-05T01:51:45.418628",
    "updated_at": "2023-04-05T01:51:45.418628"
  },
  {
    "title": "Primeiro Artigo de Teste",
    "description": "Somente um artigo para testar",
    "url_font": "http://www.chegouemail.com.br/news/L1-88-2-H.html",
    "id": 2,
    "user_id": 1,
    "created_at": "2023-04-05T01:51:52.503908",
    "updated_at": "2023-04-05T01:51:52.503908"
  }
]
```

- Na rota **/api/v1/artigos/{article_id}** é possível atualizar um artigo com o método PUT, basta informar o ID do
  artigo que deseja
  atualizar.

- Na rota **/api/v1/artigos/{article_id}** é possível deletar um artigo com o método DELETE, basta informar o ID do
  artigo que deseja
  deletar.

## 🛠️ Bibliotecas Utilizadas

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Pydantic](https://pydantic-docs.helpmanual.io/)
- [Uvicorn](https://www.uvicorn.org/)
- [psycopg2-binary](https://pypi.org/project/psycopg2-binary/)
- [asyncpg](https://pypi.org/project/asyncpg/)
- [bcrypt](https://pypi.org/project/bcrypt/)
- [python-jose](https://pypi.org/project/python-jose/)
- [passlib](https://pypi.org/project/passlib/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)
- [python-multipart](https://pypi.org/project/python-multipart/)
- [email-validator](https://pypi.org/project/email-validator/)

## 👨‍💻 Contato

- [Email](mailto:matheusfeu@gmail.com)
- [Linkedin](https://www.linkedin.com/in/matheus-feu-558558186/)
- [Github](https://github.com/matheus-feu)
- [Instagram](https://www.instagram.com/math_feu/)
