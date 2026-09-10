from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.database.connection import get_db
from app.database.models import Conta, Transacao
from app.schemas.conta import TransacaoCreate
from app.security.auth import get_usuario_atual


router = APIRouter(
    prefix="/transacoes",
    tags=["Transações"]
)


@router.post("/")
def criar_transacao(
    transacao: TransacaoCreate,
    db: Session = Depends(get_db),
    usuario_atual: str = Depends(get_usuario_atual)
):
    conta = db.query(Conta).filter(
        Conta.id == transacao.conta_id
    ).first()

    if conta is None:
        raise HTTPException(
            status_code=404,
            detail="Conta não encontrada"
        )

    if transacao.tipo == "deposito":
        conta.saldo += transacao.valor

    else:
        if conta.saldo < transacao.valor:
            raise HTTPException(
                status_code=400,
                detail="Saldo insuficiente"
            )

        conta.saldo -= transacao.valor

    nova_transacao = Transacao(
        tipo=transacao.tipo,
        valor=transacao.valor,
        conta_id=transacao.conta_id
    )

    db.add(nova_transacao)

    try:
        db.commit()
        db.refresh(nova_transacao)

    except SQLAlchemyError:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Não foi possível realizar a transação"
        )

    return {
        "message": "Transação realizada com sucesso!",
        "id": nova_transacao.id,
        "saldo_atual": conta.saldo
    }

