from passlib.context import CryptContext
from jose import jwt, JWTError
from fastapi import HTTPException, status , Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timedelta ,timezone
from dotenv import load_dotenv
import os

load_dotenv()

security = HTTPBearer()

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def criar_hash_senha(senha: str):
    return pwd_context.hash(senha)

def verificar_senha(senha: str, senha_hash: str):
    return pwd_context.verify(senha, senha_hash)

from jose import jwt


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

def criar_token(username: str):
    expiracao = datetime.now(timezone.utc) + timedelta(minutes=30)

    dados = {
        "sub": username,
        "exp": expiracao
    }

    token = jwt.encode(
        dados,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token

def verificar_token(token: str):
    try:
        dados = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        username = dados.get("sub")

        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido"
            )

        return username

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )

def get_usuario_atual(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    return verificar_token(credentials.credentials)