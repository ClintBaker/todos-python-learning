from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Path, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from db.database import SessionLocal
from db.models import Todos
from .auth import get_current_user

router = APIRouter(
    prefix='/todos',
    tags=['todos']
)



# open connection to the database (and close it when the function is done)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# dependency injection
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

# pydantics request models
class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool = False

@router.get('/', status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication required')
    return db.query(Todos).filter(Todos.owner_id == user.get('id')).all()

@router.get('/todo/{todo_id}')
async def read_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0), status_code=status.HTTP_200_OK):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication required')
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Todo not found')
    return todo_model

@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_dependency, db: db_dependency, todo_request: TodoRequest):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication required')
    todo_model = Todos(**todo_request.model_dump(), owner_id=user.get('id'))
    try:
        db.add(todo_model)
        db.commit()
        return todo_model
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put('/{todo_id}', status_code=status.HTTP_200_OK)
async def update_todo(user: user_dependency, db: db_dependency, todo_request: TodoRequest, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication required')
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Todo not found')
    setattr(todo_model, 'title', todo_request.title)
    setattr(todo_model, 'description', todo_request.description)
    setattr(todo_model, 'priority', todo_request.priority)
    setattr(todo_model, 'complete', todo_request.complete)
    db.commit()
    return {'message': 'Todo updated successfully'}

@router.delete('/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication required')
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Todo not found')
    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()
    return {'message': 'Todo deleted successfully'}