from fastapi import FastAPI
from app.routers import pratica

app = FastAPI(title="Prática FastAPI + Redis")

app.include_router(pratica.router)
