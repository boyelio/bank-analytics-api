from pydantic import BaseModel, Field, field_validator
import re


class UsuarioCreate(BaseModel):
    username: str = Field(min_length=3, max_length=30)
    senha: str = Field(min_length=8, max_length=72)

    @field_validator("senha")
    @classmethod
    def validar_senha(cls, senha):
        if " " in senha:
            raise ValueError("A senha não pode conter espaços")

        if not re.search(r"[A-Z]", senha):
            raise ValueError(
                "A senha deve conter pelo menos uma letra maiúscula"
            )

        if not re.search(r"[a-z]", senha):
            raise ValueError(
                "A senha deve conter pelo menos uma letra minúscula"
            )

        if not re.search(r"\d", senha):
            raise ValueError(
                "A senha deve conter pelo menos um número"
            )

        if not re.search(
            r"[!@#$%^&*(),.?\":{}|<>_\-+=/\\[\];']",
            senha
        ):
            raise ValueError(
                "A senha deve conter pelo menos um caractere especial"
            )

        return senha


class LoginRequest(BaseModel):
    username: str = Field(min_length=3, max_length=30)
    senha: str = Field(min_length=1, max_length=72)