from fastapi import APIRouter, status, HTTPException
from pydantic import BaseModel
from db.models import Users
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi import Depends
from typing import Annotated
from db.database import SessionLocal
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import timedelta, datetime, timezone

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

# this should be in a .env file
SECRET_KEY = '1234567890'
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

class UserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str

class Token(BaseModel):
    access_token: str
    token_type: str

# open connection to the database (and close it when the function is done)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# dependency injection
db_dependency = Annotated[Session, Depends(get_db)]

# authenticate user
def authenticate_user(username: str, password: str, db: db_dependency):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, str(user.hashed_password)):
        return False
    return user

def create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id, 'role': role}
    expire = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expire})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get('sub')
        user_id = payload.get('id')
        user_role = payload.get('role')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate credentials')
        return {'username': username, 'id': user_id, 'user_role': user_role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate credentials')


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, user: UserRequest):
    user_request = Users(
        email=user.email,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        hashed_password=bcrypt_context.hash(user.password),
        is_active=True,
        role=user.role
    )
    db.add(user_request)
    db.commit()
    return {'message': 'User created successfully'}

@router.post('/token', response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate credentials')
    username = getattr(user, 'username')
    user_id = getattr(user, 'id')
    user_role = getattr(user, 'role')
    token = create_access_token(username, user_id, user_role, timedelta(minutes=20))
    return {'access_token': token, 'token_type': 'bearer'}