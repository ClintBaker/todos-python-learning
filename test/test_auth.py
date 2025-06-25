from test.utils import *
from routers.auth import get_db, authenticate_user, create_access_token, SECRET_KEY, ALGORITHM
from db.models import Users
from passlib.context import CryptContext
import pytest
from jose import jwt
from datetime import timedelta

app.dependency_overrides[get_db] = override_get_db

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

@pytest.fixture
def test_user():
    user = Users(
        email='test@example.com',
        username='testuser',
        first_name='Test',
        last_name='User',
        hashed_password=bcrypt_context.hash('password'),
        is_active=True,
        role='user'
    )
    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    db.delete(user)
    db.commit()

def test_authenticate_user_success(test_user):
    db = TestingSessionLocal()
    
    authenticated_user = authenticate_user(test_user.username, 'password', db)
    assert authenticated_user is not None
    assert authenticated_user is not False
    assert authenticated_user.username is not None
    assert authenticated_user.username == test_user.username

def test_authenticate_user_failure(test_user):
    db = TestingSessionLocal()

    non_existing_user = authenticate_user(test_user.username, 'wrong password', db)
    assert non_existing_user is False

def test_create_access_token_success(test_user):
    username = 'testuser'
    user_id = 1
    role = 'user'
    expires_delta = timedelta(days=1)

    token = create_access_token(username, user_id, role, expires_delta)

    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={'verify_signature': False})

    assert payload['sub'] == username
    assert payload['id'] == user_id
    assert payload['role'] == role




