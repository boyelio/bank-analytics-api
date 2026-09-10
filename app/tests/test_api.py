from fastapi.testclient import TestClient
from app.database.models import Cliente, Conta , Usuario
from datetime import datetime, timedelta, timezone
from app.main import app
from app.security.auth import criar_hash_senha, criar_token



def test_status(client):
    response = client.get("/status")

    assert response.status_code == 200
    assert response.json()["status"] == "online"

def test_cliente_nao_encontrado(client):
    response = client.get("/clientes/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Cliente não encontrado"

def test_saque_com_saldo_insuficiente(client, db, auth_headers):
    cliente = Cliente(
        nome="Cliente Teste",
        cpf="99999999999",
        email="teste@teste.com"
    )

    db.add(cliente)
    db.commit()
    db.refresh(cliente)

    conta = Conta(
        numero="99999",
        tipo="corrente",
        saldo=100,
        cliente_id=cliente.id
    )

    db.add(conta)
    db.commit()
    db.refresh(conta)
    response = client.post(
        "/transacoes",
        json={
            "tipo": "saque",
            "valor": 999999,
            "conta_id": conta.id
        },
        headers=auth_headers
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Saldo insuficiente"

def test_deposito_aumenta_saldo(client, db, auth_headers):
    cliente = Cliente(
        nome="Cliente Teste",
        cpf="88888888888",
        email="deposito@teste.com"
    )

    db.add(cliente)
    db.commit()
    db.refresh(cliente)

    conta = Conta(
        numero="88888",
        tipo="corrente",
        saldo=0,
        cliente_id=cliente.id
    )

    db.add(conta)
    db.commit()
    db.refresh(conta)

    response = client.post(
        "/transacoes",
        json={
            "tipo": "deposito",
            "valor": 100,
            "conta_id": conta.id
        },
        headers=auth_headers
    )

    assert response.status_code == 200
    assert response.json()["saldo_atual"] == 100

def test_transacao_com_valor_invalido(client, db , auth_headers):
    cliente = Cliente(
        nome="Cliente Teste",
        cpf="77777777777",
        email="valor@teste.com"
    )

    db.add(cliente)
    db.commit()
    db.refresh(cliente)

    conta = Conta(
        numero="77777",
        tipo="corrente",
        saldo=100,
        cliente_id=cliente.id
    )

    db.add(conta)
    db.commit()
    db.refresh(conta)

    response = client.post(
        "/transacoes",
        json={
            "tipo": "deposito",
            "valor": -100,
            "conta_id": conta.id
        },
        headers=auth_headers
    )

    assert response.status_code == 422
    assert "O valor deve ser maior que zero" in response.json()["detail"][0]["msg"]

def test_tipo_transacao_invalido(client, db, auth_headers):

    cliente = Cliente(
        nome="Cliente Teste",
        cpf="66666666666",
        email="tipo@teste.com"
    )

    db.add(cliente)
    db.commit()
    db.refresh(cliente)

    conta = Conta(
        numero="66666",
        tipo="corrente",
        saldo=100,
        cliente_id=cliente.id
    )

    db.add(conta)
    db.commit()
    db.refresh(conta)

    response = client.post(
        "/transacoes",
        json={
            "tipo": "pix",
            "valor": 100,
            "conta_id": conta.id
        },
        headers=auth_headers
    )

    assert response.status_code == 422
    assert "O tipo deve ser 'deposito' ou 'saque'" in response.json()["detail"][0]["msg"]

def test_clientes_sem_token(client):
    response = client.get("/clientes")

    assert response.status_code == 401

