FROM python:3.12-slim

WORKDIR /app

# Instala o Poetry
RUN pip install poetry

# Copia os arquivos de dependências primeiro (aproveita o cache do Docker)
COPY pyproject.toml poetry.lock* ./

# Instala as dependências direto no ambiente do container
RUN poetry config virtualenvs.create false \
      && poetry install --no-interaction --no-ansi --no-root

# Copia o restante do código
COPY . .

# Inicia o servidor FastAPI
CMD ["fastapi", "run", "main.py", "--port", "8000"]
