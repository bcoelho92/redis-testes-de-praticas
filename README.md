# 🚀 Práticas com Redis e FastAPI

Repositório de estudos práticos explorando padrões essenciais de uso do **Redis** integrado a uma API assíncrona com **FastAPI** e Python 3.12.

---

## 📌 Cenários Práticos Implementados

Este projeto aborda 4 padrões comuns de uso do Redis no dia a dia de engenharia de software:

1. **Health Check & Conectividade (`/pratica/health`)**
   - Validação da conexão ativa com o servidor Redis via `redis_client.ping()`.
2. **Cache-Aside com Expiração (TTL) (`/pratica/produtos/{produto_id}`)**
   - Simulação de consulta demorada a banco de dados (3s).
   - Armazenamento em cache JSON no Redis com expiração automática de 30 segundos (`set(..., ex=30)`).
   - Respostas subsequentes servidas instantaneamente da memória.
3. **Rate Limiting (Limitador de Requisições) (`/pratica/recurso-protegido`)**
   - Controle de taxa de requisições por usuário utilizando operações atômicas `INCR` e `EXPIRE`.
   - Limite de até 5 requisições por janela de 60 segundos, retornando `HTTP 429 Too Many Requests` quando excedido.
4. **Fila de Mensagens / Tarefas FIFO (`/pratica/tarefas/*`)**
   - Padrão produtor/consumidor utilizando listas Redis (`LPUSH` para enfileirar e `RPOP` para desenfileirar).
   - `POST /pratica/tarefas/enfileirar`: Adiciona nova tarefa à fila.
   - `POST /pratica/tarefas/processar-proxima`: Consome e processa o item mais antigo pendente.

---

## 🛠️ Tecnologias

- **Python 3.12**
- **FastAPI**
- **redis-py** (cliente assíncrono `redis.asyncio`)
- **Poetry** (gerenciador de dependências e ambiente)
- **Docker & Docker Compose** (Redis 7 Alpine + container da API)

---

## 📁 Estrutura do Projeto

```text
.
├── app/
│   ├── __init__.py
│   ├── redis_client.py       # Configuração e instância assíncrona do Redis
│   └── routers/
│       ├── __init__.py
│       └── pratica.py        # Rotas com os padrões práticos
├── docker-compose.yml        # Orquestração do Redis e da API
├── Dockerfile                # Imagem de build da API
├── main.py                   # Ponto de entrada do FastAPI
├── pyproject.toml            # Configuração e dependências Poetry
└── README.md
```

---

## 🚀 Como Executar

### Pré-requisitos
- [Docker](https://docs.docker.com/get-docker/) e [Docker Compose](https://docs.docker.com/compose/) instalados, ou Python 3.12+ e [Poetry](https://python-poetry.org/).

---

### Opção 1: Via Docker Compose (Recomendado)

Sobe o container do Redis e o container da API de uma só vez:

```bash
docker compose up --build
```

- **API FastAPI:** `http://localhost:8000`
- **Documentação Swagger (OpenAPI):** [http://localhost:8000/docs](http://localhost:8000/docs)
- **Redis Host Port:** `localhost:6380` (mapeada internamente para `6379`)

Para parar os serviços:
```bash
docker compose down
```

---

### Opção 2: Execução Local (Desenvolvimento)

1. **Suba apenas o serviço do Redis:**
   ```bash
   docker compose up -d redis
   ```
   *(Ou utilize uma instância local do Redis rodando na porta 6380).*

2. **Instale as dependências com o Poetry:**
   ```bash
   poetry install
   ```

3. **Inicie o servidor FastAPI em modo de desenvolvimento:**
   ```bash
   poetry run fastapi dev main.py
   ```
   *Nota: Por padrão, `app/redis_client.py` busca `REDIS_HOST=localhost` e `REDIS_PORT=6380` caso não sejam fornecidas variáveis de ambiente.*

---

## 🧪 Testando os Endpoints

Você pode testar interativamente pela interface do **Swagger** em [http://localhost:8000/docs](http://localhost:8000/docs) ou via terminal:

### 1. Health Check
```bash
curl -X GET http://localhost:8000/pratica/health
```

### 2. Cache com TTL (Produto)
```bash
# 1ª chamada: demora ~3 segundos (origem: banco_de_dados)
curl -X GET http://localhost:8000/pratica/produtos/1

# 2ª chamada (dentro de 30s): resposta imediata (origem: cache (Redis))
curl -X GET http://localhost:8000/pratica/produtos/1
```

### 3. Rate Limit
```bash
# Execute múltiplas vezes seguidas para ver o contador e o bloqueio com status 429 após 5 tentativas:
curl -X GET "http://localhost:8000/pratica/recurso-protegido?usuario_id=user_1"
```

### 4. Fila de Tarefas (FIFO)
```bash
# Enfileirar tarefa:
curl -X POST "http://localhost:8000/pratica/tarefas/enfileirar?descricao=Enviar%20email%20de%20boas-vindas"

# Processar próxima tarefa:
curl -X POST http://localhost:8000/pratica/tarefas/processar-proxima
```

---

## 📚 Referências

- [Documentação Oficial do Redis](https://redis.io/docs/latest/get-started/)
- [Documentação do FastAPI](https://fastapi.tiangolo.com/)
- [redis-py (Async IO Documentation)](https://redis.readthedocs.io/en/stable/)
