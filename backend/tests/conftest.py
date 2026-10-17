import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.db.session import Base, get_db
from app.main import app

# StaticPool ensures the in-memory SQLite database is shared across threads and sessions
engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session", autouse=True)
def init_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db():
    session = TestingSessionLocal()
    yield session
    session.close()


@pytest.fixture(scope="function")
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def auth_headers(client):
    # Register test user
    client.post("/api/v1/auth/register", json={
        "email": "test@contextpilot.ai",
        "password": "Password123!",
        "full_name": "Test Engineer"
    })
    # Login
    res = client.post("/api/v1/auth/login", json={
        "email": "test@contextpilot.ai",
        "password": "Password123!"
    })
    token = res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def second_user_headers(client):
    # Register second user for tenant isolation tests
    client.post("/api/v1/auth/register", json={
        "email": "user2@contextpilot.ai",
        "password": "Password123!",
        "full_name": "Second User"
    })
    res = client.post("/api/v1/auth/login", json={
        "email": "user2@contextpilot.ai",
        "password": "Password123!"
    })
    token = res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
