from fastapi import FastAPI

from app.database.connection import engine
from app.database.models import Base

from app.routers import (
    auth,
    clientes,
    contas,
    transacoes,
    analytics
)


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Bank Analytics API",
    version="1.0.0",
    description="API bancária desenvolvida com FastAPI, PostgreSQL, SQLAlchemy e Pandas."
)


app.include_router(auth.router)
app.include_router(clientes.router)
app.include_router(contas.router)
app.include_router(transacoes.router)
app.include_router(analytics.router)


@app.get("/")
def home():
    return {
        "message": "Bank Analytics API funcionando!"
    }


@app.get("/status")
def status():
    return {
        "status": "online",
        "projeto": "Bank Analytics API"
    }