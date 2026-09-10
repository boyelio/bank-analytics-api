from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import pandas as pd

from app.database.connection import get_db
from app.database.models import Transacao, Conta, Cliente
from app.security.auth import get_usuario_atual


router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)


@router.get("/transacoes")
def analytics_transacoes(
    db: Session = Depends(get_db),
    usuario_atual: str = Depends(get_usuario_atual)
):
    transacoes = db.query(Transacao).all()

    if not transacoes:
        return {
            "quantidade_transacoes": 0,
            "quantidade_depositos": 0,
            "quantidade_saques": 0,
            "total_depositado": 0,
            "total_sacado": 0,
            "valor_medio": 0,
            "transacoes_alto_valor": 0,
            "transacoes_alto_risco": 0,
            "resumo_contas": []
        }

    df = pd.DataFrame([
        {
            "id": t.id,
            "tipo": t.tipo,
            "valor": float(t.valor),
            "conta_id": t.conta_id
        }
        for t in transacoes
    ])

    quantidade_transacoes = len(df)

    quantidade_depositos = len(
        df[df["tipo"] == "deposito"]
    )

    quantidade_saques = len(
        df[df["tipo"] == "saque"]
    )

    total_depositado = df.loc[
        df["tipo"] == "deposito",
        "valor"
    ].sum()

    total_sacado = df.loc[
        df["tipo"] == "saque",
        "valor"
    ].sum()

    valor_medio = df["valor"].mean()

    transacoes_alto_valor = len(
        df[df["valor"] > 5000]
    )

    df["risco_pontos"] = 0

    df.loc[
        df["valor"] > 5000,
        "risco_pontos"
    ] += 2

    df.loc[
        df["valor"] > 10000,
        "risco_pontos"
    ] += 3

    df.loc[
        df["tipo"] == "saque",
        "risco_pontos"
    ] += 1

    def classificar_risco(pontos):
        if pontos >= 5:
            return "ALTO"
        elif pontos >= 3:
            return "MEDIO"
        else:
            return "BAIXO"

    df["risco"] = df["risco_pontos"].apply(
        classificar_risco
    )

    transacoes_alto_risco = len(
        df[df["risco"] == "ALTO"]
    )

    df_contas = pd.DataFrame([
        {
            "id": conta.id,
            "numero": conta.numero,
            "cliente_id": conta.cliente_id
        }
        for conta in db.query(Conta).all()
    ])

    resumo_contas = (
        df.groupby("conta_id")
        .agg(
            quantidade_transacoes=("id", "count"),
            total_movimentado=("valor", "sum"),
            valor_medio=("valor", "mean")
        )
        .reset_index()
    )

    if not df_contas.empty:
        resumo_contas = resumo_contas.merge(
            df_contas,
            left_on="conta_id",
            right_on="id",
            how="left"
        )

        resumo_contas = resumo_contas.rename(
            columns={
                "cliente_id": "cliente_id",
                "numero": "numero_conta"
            }
        )

    return {
        "quantidade_transacoes": quantidade_transacoes,
        "quantidade_depositos": quantidade_depositos,
        "quantidade_saques": quantidade_saques,
        "total_depositado": total_depositado,
        "total_sacado": total_sacado,
        "valor_medio": valor_medio,
        "transacoes_alto_valor": transacoes_alto_valor,
        "transacoes_alto_risco": transacoes_alto_risco,
        "resumo_contas": resumo_contas.to_dict(
            orient="records"
        )
    }


@router.get("/clientes")
def analytics_clientes(
    db: Session = Depends(get_db),
    usuario_atual: str = Depends(get_usuario_atual)
):
    transacoes = db.query(Transacao).all()
    contas = db.query(Conta).all()
    clientes = db.query(Cliente).all()

    if not transacoes:
        return []

    df_transacoes = pd.DataFrame([
        {
            "id": t.id,
            "tipo": t.tipo,
            "valor": float(t.valor),
            "conta_id": t.conta_id
        }
        for t in transacoes
    ])

    df_contas = pd.DataFrame([
        {
            "id": conta.id,
            "numero": conta.numero,
            "cliente_id": conta.cliente_id
        }
        for conta in contas
    ])

    df_clientes = pd.DataFrame([
        {
            "id": cliente.id,
            "nome": cliente.nome,
            "cpf": cliente.cpf,
            "email": cliente.email
        }
        for cliente in clientes
    ])

    df = df_transacoes.merge(
        df_contas,
        left_on="conta_id",
        right_on="id",
        how="left"
    )

    df = df.merge(
        df_clientes,
        left_on="cliente_id",
        right_on="id",
        how="left"
    )

    resumo = (
        df.groupby(
            ["cliente_id", "nome"]
        )
        .agg(
            quantidade_transacoes=("id_x", "count"),
            total_movimentado=("valor", "sum"),
            valor_medio=("valor", "mean")
        )
        .reset_index()
    )

    resumo["risco_pontos"] = 0

    resumo.loc[
        resumo["total_movimentado"] > 5000,
        "risco_pontos"
    ] += 2

    resumo.loc[
        resumo["total_movimentado"] > 10000,
        "risco_pontos"
    ] += 3

    def classificar_risco(pontos):
        if pontos >= 5:
            return "ALTO"
        elif pontos >= 3:
            return "MEDIO"
        else:
            return "BAIXO"

    resumo["risco"] = resumo["risco_pontos"].apply(
        classificar_risco
    )

    return resumo[
        [
            "cliente_id",
            "nome",
            "quantidade_transacoes",
            "total_movimentado",
            "valor_medio",
            "risco"
        ]
    ].to_dict(
        orient="records"
    )