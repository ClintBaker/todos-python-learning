from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from db.database import Base
from main import app
from fastapi.testclient import TestClient
import pytest
from db.models import Todos

SQLALCHEMY_DATABASE_URL="sqlite:///./test/test.db"      

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False}, poolclass=StaticPool)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

def override_get_current_user():
    return {'username': 'testuser', 'id': 1, 'user_role': 'admin'}

client = TestClient(app)

@pytest.fixture
def test_todo():
    todo = Todos(title='Test Todo', description='Test Description', priority=1, complete=False, owner_id=1)
    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo 
    with engine.connect() as conn:
        conn.execute(text('DELETE FROM todos'))
        conn.commit()