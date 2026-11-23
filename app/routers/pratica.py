import asyncio
import json
import app
from fastapi import APIRouter, HTTPException
from app.redis_client import redis_client

router = APIRouter(prefix="/pratica", tags=["Prática FastAPI + Redis"])

@router.get("/health")
async def health_check():
    try:
        conectado = await redis_client.ping()
        return {"status": "ok", "redis_conectado": conectado}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Erro ao conectar no Redis: {str(e)}")

# ... (aqui entram as outras rotas de /produtos, /recurso-protegido e /tarefas usando @router)

async def buscar_produto_no_banco(produto_id: int):
    await asyncio.sleep(3)  # Simula 3 segundos de lentidão
    return {
        "id": produto_id,
        "nome": f"Teclado Mecânico v{produto_id}",
        "preco": 350.00
      }

@router.get("/produtos/{produto_id}")
async def obter_produto(produto_id: int):
    chave_cache = f"produto:{produto_id}"

    # 1. Tenta buscar no Redis
    dados_cache = await redis_client.get(chave_cache)
    if dados_cache:
        return {"origem": "cache (Redis)", "dados": json.loads(dados_cache)}

    # 2. Se não achou, busca no "banco"
    produto = await buscar_produto_no_banco(produto_id)

    # 3. Salva no Redis com expiração de 30 segundos (ex=30)
    await redis_client.set(chave_cache, json.dumps(produto), ex=30)

    return {"origem": "banco_de_dados", "dados": produto}


@router.get("/recurso-protegido")
async def acessar_recurso(usuario_id: str = "user_1"):
    chave = f"rate_limit:{usuario_id}"
    
    # Incrementa o contador de acessos desse usuário
    requisicoes = await redis_client.incr(chave)
    
    # Se for a primeira requisição, iniciamos o cronômetro de 60 segundos
    if requisicoes == 1:
        await redis_client.expire(chave, 60)
        
    # TODO: Verificar se passou do limite de 5 requisições
    if requisicoes > 5:
      raise HTTPException(
          status_code=429, detail="Limite de requisições excedido. Tente novamente mais tarde."
      )

    return {"mensagem": "Acesso permitido!", "tentativa": requisicoes}


@router.post("/tarefas/enfileirar")
async def adicionar_tarefa(descricao: str):
    # Coloca a tarefa na ponta esquerda da lista 'fila_emails'
    tamanho_fila = await redis_client.lpush("fila_emails", descricao)
    return {
        "mensagem": "Tarefa adicionada na fila com sucesso!",
        "posicao_na_fila": tamanho_fila
    }

@router.post("/tarefas/processar-proxima")
async def processar_tarefa():
    # TODO: Retirar o item mais antigo da ponta direita da lista 'fila_emails'
    tarefa = await redis_client.rpop("fila_emails")

    if not tarefa:
        return {"mensagem": "Nenhuma tarefa pendente na fila."}
        
    return {"mensagem": "Tarefa processada!", "tarefa_executada": tarefa}
