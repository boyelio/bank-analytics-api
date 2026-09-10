from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import declarative_base , relationship

Base = declarative_base()


class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    cpf = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)

    contas = relationship("Conta", back_populates="cliente")

class Conta(Base):
    __tablename__ = "contas"

    id = Column(Integer, primary_key=True, index=True)
    numero = Column(String, unique=True, nullable=False)
    tipo = Column(String, nullable=False)
    saldo = Column(Numeric, default=0)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)

    cliente = relationship("Cliente", back_populates="contas")

class Transacao(Base):
    __tablename__ = "transacoes"

    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String, nullable=False)
    valor = Column(Numeric, nullable=False)
    conta_id = Column(Integer, ForeignKey("contas.id"), nullable=False)

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    senha_hash = Column(String, nullable=False)