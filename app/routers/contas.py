from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.database.models import Cliente, Conta, Transacao
from app.database.connection import get_db
from app.database.models import Cliente, Conta
from app.schemas.conta import ContaCreate, ContaResponse
from app.security.auth import get_usuario_atual


router = APIRouter(
    prefix="/contas",
    tags=["Contas"]
)


@router.post("/", response_model=ContaResponse)
def criar_conta(
    conta: ContaCreate,
    db: Session = Depends(get_db),
    usuario_atual: str = Depends(get_usuario_atual)
):
    cliente = db.query(Cliente).filter(
        Cliente.id == conta.cliente_id
    ).first()

    if cliente is None:
        raise HTTPException(
            status_code=404,
            detail="Cliente não encontrado"
        )

    conta_existente = db.query(Conta).filter(
        Conta.numero == conta.numero
    ).first()

    if conta_existente:
        raise HTTPException(
            status_code=400,
            detail="Número da conta já está cadastrado"
        )

    nova_conta = Conta(
        numero=conta.numero,
        tipo=conta.tipo,
        saldo=0,
        cliente_id=conta.cliente_id
    )

    db.add(nova_conta)

    try:
        db.commit()
        db.refresh(nova_conta)

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=400,
            detail="Número da conta já está cadastrado"
        )

    return nova_conta


@router.get("/", response_model=list[ContaResponse])
def listar_contas(
    db: Session = Depends(get_db),
    usuario_atual: str = Depends(get_usuario_atual)
):
    contas = db.query(Conta).all()

    return contas

@router.get("/{conta_id}/transacoes")
def listar_transacoes(
    conta_id: int,
    db: Session = Depends(get_db)
):
    conta = db.query(Conta).filter(
        Conta.id == conta_id
    ).first()

    if conta is None:
        raise HTTPException(
            status_code=404,
            detail="Conta não encontrada"
        )

    transacoes = db.query(Transacao).filter(
        Transacao.conta_id == conta_id
    ).all()

    return transacoes