import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.main import app
from app.database.connection import get_db
from app.database.models import Base , Usuario
from app.security.auth import criar_hash_senha , criar_token


DATABASE_URL_TEST = "postgresql://postgres:postgres@localhost:5432/bank_analytics_test"

engine_test = create_engine(DATABASE_URL_TEST)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine_test
)


@pytest.fixture
def db():
    Base.metadata.create_all(bind=engine_test)

    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine_test)


@pytest.fixture
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    return TestClient(app)

@pytest.fixture
def auth_headers(db):
    usuario = Usuario(
        username="usuario_teste",
        senha_hash=criar_hash_senha("123456")
    )

    db.add(usuario)
    db.commit()
    db.refresh(usuario)

    token = criar_token(usuario.username)

    return {
        "Authorization": f"Bearer {token}"
    }