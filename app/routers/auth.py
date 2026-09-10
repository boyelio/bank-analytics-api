from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.schemas.usuario import UsuarioCreate, LoginRequest
from app.database.connection import get_db
from app.database.models import Usuario
from app.security.auth import (
    verificar_senha,
    criar_token,
    criar_hash_senha
)


router = APIRouter(
    prefix="",
    tags=["Autenticação"]
)


@router.post("/usuarios")
def criar_usuario(
    usuario: UsuarioCreate,
    db: Session = Depends(get_db)
):
    usuario_existente = db.query(Usuario).filter(
        Usuario.username == usuario.username
    ).first()

    if usuario_existente:
        raise HTTPException(
            status_code=400,
            detail="Username já está em uso"
        )

    senha_hash = criar_hash_senha(usuario.senha)

    novo_usuario = Usuario(
        username=usuario.username,
        senha_hash=senha_hash
    )

    db.add(novo_usuario)

    try:
        db.commit()
        db.refresh(novo_usuario)

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=400,
            detail="Não foi possível criar o usuário"
        )

    return {
        "message": "Usuário criado com sucesso!",
        "id": novo_usuario.id,
        "username": novo_usuario.username
    }


@router.post("/login")
def login(
    usuario: LoginRequest,
    db: Session = Depends(get_db)
):
    usuario_db = db.query(Usuario).filter(
        Usuario.username == usuario.username
    ).first()

    if usuario_db is None:
        raise HTTPException(
            status_code=401,
            detail="Usuário ou senha inválidos"
        )

    if not verificar_senha(
        usuario.senha,
        usuario_db.senha_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Usuário ou senha inválidos"
        )

    token = criar_token(usuario_db.username)

    return {
        "access_token": token,
        "token_type": "bearer"
    }