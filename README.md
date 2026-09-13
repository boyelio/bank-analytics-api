# Bank Analytics API

API bancária desenvolvida em Python com FastAPI, PostgreSQL e SQLAlchemy, com autenticação JWT, transações financeiras, análise de dados com Pandas, testes automatizados e execução via Docker.

## Tecnologias

* Python 3.13
* FastAPI
* PostgreSQL
* SQLAlchemy
* Pandas
* Pydantic
* JWT
* Passlib / bcrypt
* Pytest
* Docker
* Docker Compose

## Funcionalidades

### Autenticação

* Cadastro de usuários
* Hash seguro de senhas com bcrypt
* Login
* Geração de token JWT
* Proteção de endpoints autenticados

### Clientes

* Criar cliente
* Listar clientes
* Buscar cliente por ID
* Atualizar cliente
* Deletar cliente
* Validação de CPF e e-mail

### Contas

* Criar conta bancária
* Listar contas
* Consultar transações de uma conta
* Associação entre cliente e conta

### Transações

* Depósitos
* Saques
* Validação de saldo
* Atualização automática do saldo da conta
* Registro das movimentações
* Rollback em caso de erro no banco de dados

### Analytics

A API utiliza Pandas para gerar análises das movimentações bancárias.

Entre as métricas disponíveis estão:

* Quantidade de transações
* Quantidade de depósitos
* Quantidade de saques
* Total depositado
* Total sacado
* Valor médio das transações
* Transações de alto valor
* Classificação de risco
* Resumo de movimentações por conta
* Análise de movimentações por cliente

## Estrutura do projeto

```text
BANK_ANALYTICS_API/
│
├── app/
│   ├── main.py
│   │
│   ├── routers/
│   │   ├── auth.py
│   │   ├── clientes.py
│   │   ├── contas.py
│   │   ├── transacoes.py
│   │   └── analytics.py
│   │
│   ├── schemas/
│   │   ├── cliente.py
│   │   ├── conta.py
│   │   └── usuario.py
│   │
│   ├── database/
│   │   ├── connection.py
│   │   └── models.py
│   │
│   ├── security/
│   │   └── auth.py
│   │
│   └── tests/
│       ├── conftest.py
│       └── test_api.py
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .dockerignore
├── .gitignore
└── README.md
```

## Executando com Docker

É necessário possuir Docker Desktop instalado.

Clone o projeto:

```bash
git clone <https://github.com/boyelio/bank-analytics-api>
cd BANK_ANALYTICS_API
```

Crie um arquivo `.env`:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/bank_analytics
SECRET_KEY=sua_chave_secreta
```

Suba os containers:

```bash
docker compose up --build
```

A API estará disponível em:

```text
http://localhost:8000
```

Documentação Swagger:

```text
http://localhost:8000/docs
```

## Testes

Para executar os testes:

```bash
python -m pytest
```

O projeto utiliza um banco PostgreSQL separado para os testes, evitando alterações no banco principal.

## Principais endpoints

| Método | Endpoint                  | Descrição                  |
| ------ | ------------------------- | -------------------------- |
| POST   | `/usuarios`               | Criar usuário              |
| POST   | `/login`                  | Fazer login                |
| GET    | `/clientes/`              | Listar clientes            |
| POST   | `/clientes/`              | Criar cliente              |
| GET    | `/clientes/{id}`          | Buscar cliente             |
| PUT    | `/clientes/{id}`          | Atualizar cliente          |
| DELETE | `/clientes/{id}`          | Deletar cliente            |
| GET    | `/contas/`                | Listar contas              |
| POST   | `/contas/`                | Criar conta                |
| GET    | `/contas/{id}/transacoes` | Listar transações da conta |
| POST   | `/transacoes/`            | Realizar depósito ou saque |
| GET    | `/analytics/transacoes`   | Analytics das transações   |
| GET    | `/analytics/clientes`     | Analytics dos clientes     |

## Objetivo do projeto

O projeto foi desenvolvido com o objetivo de praticar conceitos utilizados no desenvolvimento backend, incluindo:

* APIs REST
* Arquitetura em camadas
* Bancos de dados relacionais
* ORM
* Autenticação
* Segurança de senhas
* Tratamento de erros
* Transações de banco de dados
* Análise de dados
* Testes automatizados
* Containerização

## Próximas melhorias

* Alembic para migrations
* Mais testes automatizados
* Paginação de clientes e contas
* Logs da aplicação
* CI/CD com GitHub Actions
* Deploy em ambiente cloud

---

Projeto desenvolvido para estudos e portfólio de desenvolvimento Backend.
