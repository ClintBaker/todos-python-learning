from main import app
from routers.todos import get_db
from routers.auth import get_current_user
from fastapi import status
from db.models import Todos
from test.utils import *

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_read_all_authenticated(test_todo):
    response = client.get('/todos')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{'complete': False, 'description': 'Test Description', 'id': 1, 'owner_id': 1, 'priority': 1, 'title': 'Test Todo'}]

def test_read_single_todo(test_todo):
    response = client.get('/todos/todo/1')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'complete': False, 'description': 'Test Description', 'id': 1, 'owner_id': 1, 'priority': 1, 'title': 'Test Todo'}

def test_read_single_todo_not_found():
    response = client.get('/todos/todo/999')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Todo not found'}

def test_create_todo_authenticated(test_todo):
    request_data = {
        'title': 'Test Todo 2',
        'description': 'Test Description 2',
        'priority': 2,
        'complete': False,
        'owner_id': 1
    }
    response = client.post('/todos', json=request_data)
    assert response.status_code == status.HTTP_201_CREATED

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 2).first()
    assert model is not None, "Todo should be created"
    assert model.title == request_data.get('title')
    assert model.description == request_data.get('description')
    assert model.priority == request_data.get('priority')
    assert model.complete == request_data.get('complete')
    assert model.owner_id == request_data.get('owner_id')

def test_update_todo(test_todo):
    request_data = {
        'title': 'Updated Todo',
        'description': 'Updated Description',
        'priority': 3,
        'complete': True
    }
    response = client.put('/todos/1', json=request_data)
    assert response.status_code == status.HTTP_200_OK

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is not None, "Todo should be updated"
    assert model.title == request_data.get('title')
    assert model.description == request_data.get('description')
    assert model.priority == request_data.get('priority')
    assert model.complete == request_data.get('complete')

def test_update_todo_not_found():
    request_data = {
        'title': 'Updated Todo',
        'description': 'Updated Description',
        'priority': 3,
        'complete': True
    }
    response = client.put('/todos/999', json=request_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Todo not found'}

def test_delete_todo(test_todo):
    response = client.delete('/todos/1')
    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None, "Todo should be deleted"

def test_delete_todo_not_found():
    response = client.delete('/todos/999')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Todo not found'}