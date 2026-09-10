from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database.connection import get_db
from app.database.models import Cliente
from app.schemas.cliente import ClienteCreate, ClienteResponse
from app.security.auth import get_usuario_atual


router = APIRouter(
    prefix="/clientes",
    tags=["Clientes"]
)


@router.get("/", response_model=list[ClienteResponse])
def listar_clientes(
    db: Session = Depends(get_db),
    usuario_atual: str = Depends(get_usuario_atual)
):
    clientes = db.query(Cliente).all()

    return clientes


@router.post("/", response_model=ClienteResponse)
def criar_cliente(
    cliente: ClienteCreate,
    db: Session = Depends(get_db),
    usuario_atual: str = Depends(get_usuario_atual)
):
    cliente_existente = db.query(Cliente).filter(
        (Cliente.cpf == cliente.cpf) |
        (Cliente.email == cliente.email)
    ).first()

    if cliente_existente:
        raise HTTPException(
            status_code=400,
            detail="CPF ou email já está cadastrado"
        )

    novo_cliente = Cliente(
        nome=cliente.nome,
        cpf=cliente.cpf,
        email=cliente.email
    )

    db.add(novo_cliente)

    try:
        db.commit()
        db.refresh(novo_cliente)

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=400,
            detail="CPF ou email já está cadastrado"
        )

    return novo_cliente


@router.put("/{cliente_id}", response_model=ClienteResponse)
def atualizar_cliente(
    cliente_id: int,
    cliente: ClienteCreate,
    db: Session = Depends(get_db),
    usuario_atual: str = Depends(get_usuario_atual)
):
    cliente_db = db.query(Cliente).filter(
        Cliente.id == cliente_id
    ).first()

    if cliente_db is None:
        raise HTTPException(
            status_code=404,
            detail="Cliente não encontrado"
        )

    cliente_db.nome = cliente.nome
    cliente_db.cpf = cliente.cpf
    cliente_db.email = cliente.email

    try:
        db.commit()
        db.refresh(cliente_db)

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=400,
            detail="CPF ou email já está cadastrado"
        )

    return cliente_db


@router.delete("/{cliente_id}")
def deletar_cliente(
    cliente_id: int,
    db: Session = Depends(get_db),
    usuario_atual: str = Depends(get_usuario_atual)
):
    cliente = db.query(Cliente).filter(
        Cliente.id == cliente_id
    ).first()

    if cliente is None:
        raise HTTPException(
            status_code=404,
            detail="Cliente não encontrado"
        )

    db.delete(cliente)

    try:
        db.commit()

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=400,
            detail="Não foi possível deletar o cliente"
        )

    return {
        "message": "Cliente deletado com sucesso!"
    }

@router.get("/{cliente_id}", response_model=ClienteResponse)
def buscar_cliente(
    cliente_id: int,
    db: Session = Depends(get_db)
):
    cliente = db.query(Cliente).filter(
        Cliente.id == cliente_id
    ).first()

    if cliente is None:
        raise HTTPException(
            status_code=404,
            detail="Cliente não encontrado"
        )

    return cliente