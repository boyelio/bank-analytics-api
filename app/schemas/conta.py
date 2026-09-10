from decimal import Decimal

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class ContaCreate(BaseModel):
    numero: str = Field(min_length=4, max_length=20)
    tipo: str
    cliente_id: int = Field(gt=0)

    @field_validator("numero")
    @classmethod
    def validar_numero(cls, numero):
        numero = numero.strip()

        if not numero:
            raise ValueError("O número da conta não pode estar vazio")

        return numero

    @field_validator("tipo")
    @classmethod
    def validar_tipo(cls, tipo):
        tipos_validos = ["corrente", "poupanca"]

        if tipo not in tipos_validos:
            raise ValueError(
                "O tipo da conta deve ser 'corrente' ou 'poupanca'"
            )

        return tipo


class ContaResponse(BaseModel):
    id: int
    numero: str
    tipo: str
    saldo: Decimal
    cliente_id: int

    model_config = ConfigDict(from_attributes=True)


class TransacaoCreate(BaseModel):
    tipo: str
    valor: Decimal = Field(
        max_digits=12,
        decimal_places=2
    )
    conta_id: int = Field(gt=0)

    @field_validator("valor")
    @classmethod
    def validar_valor(cls, valor):
        if valor <= 0:
            raise ValueError("O valor deve ser maior que zero")

        return valor

    @field_validator("tipo")
    @classmethod
    def validar_tipo(cls, tipo):
        if tipo not in ["deposito", "saque"]:
            raise ValueError(
                "O tipo deve ser 'deposito' ou 'saque'"
            )

        return tipo