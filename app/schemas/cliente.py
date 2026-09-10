import re

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from app.schemas.conta import ContaResponse


class ClienteCreate(BaseModel):
    nome: str = Field(min_length=2, max_length=100)
    cpf: str
    email: EmailStr

    @field_validator("nome")
    @classmethod
    def validar_nome(cls, nome):
        nome = nome.strip()

        if not nome:
            raise ValueError("O nome não pode estar vazio")

        return nome

    @field_validator("cpf")
    @classmethod
    def validar_cpf(cls, cpf):
        cpf = re.sub(r"\D", "", cpf)

        if len(cpf) != 11:
            raise ValueError("O CPF deve conter 11 dígitos")

        if len(set(cpf)) == 1:
            raise ValueError("CPF inválido")

        return cpf


class ClienteResponse(BaseModel):
    id: int
    nome: str
    cpf: str
    email: EmailStr
    contas: list[ContaResponse] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)