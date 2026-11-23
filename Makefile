.PHONY: help up down restart build logs logs-api logs-redis ps redis-cli redis-monitor flush-redis install run-local clean

# Alvo padrão: exibe o menu de ajuda com descrição dos comandos
help:
	@echo "======================================================================"
	@echo "                   COMANDOS DISPONÍVEIS (MAKEFILE)                    "
	@echo "======================================================================"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

## --- Docker & Containers ---
up: ## Sobe todos os containers em background (API + Redis)
	docker compose up -d

build: ## Constrói ou reconstrói as imagens dos containers
	docker compose build

up-build: ## Reconstrói e sobe os containers em background
	docker compose up -d --build

down: ## Para e remove todos os containers da aplicação
	docker compose down

down-v: ## Para e remove containers e volumes
	docker compose down -v

restart: ## Reinicia os containers da aplicação
	docker compose restart

ps: ## Lista os containers do projeto e status de execução
	docker compose ps

logs: ## Acompanha os logs de todos os serviços em tempo real
	docker compose logs -f

logs-api: ## Acompanha os logs apenas da API FastAPI
	docker compose logs -f api

logs-redis: ## Acompanha os logs apenas do Redis
	docker compose logs -f redis

## --- Ferramentas Redis (Estudos & Debug) ---
redis-cli: ## Abre o terminal interativo redis-cli no container
	docker compose exec redis redis-cli

redis-monitor: ## Monitora todos os comandos executados no Redis em tempo real
	docker compose exec redis redis-cli MONITOR

flush-redis: ## Limpa todas as chaves e dados do Redis (FLUSHALL)
	docker compose exec redis redis-cli FLUSHALL

## --- Desenvolvimento Local (Poetry) ---
redis-up: ## Sobe apenas o container do Redis (para rodar a API localmente)
	docker compose up -d redis

install: ## Instala dependências do projeto via Poetry
	poetry install

run-local: ## Executa a API FastAPI localmente com hot-reload
	poetry run fastapi dev main.py

clean: ## Remove caches Python (__pycache__, .pytest_cache)
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
