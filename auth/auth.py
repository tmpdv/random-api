from datetime import datetime, timedelta
from typing import Union

from fastapi import HTTPException, Request, status
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from auth.dto import UserCreateForm, UserDTO, TokenData
from db.crud import save_user, get_user_by_login
from db.models import User

SECRET_KEY = "10e36d104faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

ANON_LOGIN = "anonymous"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def create_user(request: Request, db: Session):
    form = UserCreateForm(await request.body())
    form.validate()
    if len(form.errors) == 0:
        try:
            return UserDTO(save_user(User(login=form.login, email=form.email,
                                          password=get_password_hash(form.password)), db))
        except IntegrityError:
            form.errors.append('Duplicate login or email')
    raise HTTPException(status_code=400, detail=form.errors)


def credentials_exception():
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


async def get_current_user(token: str, db: Session):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        login: str = payload.get("sub")
        if login is None:
            raise credentials_exception()
        if login == ANON_LOGIN:
            user = User(login=ANON_LOGIN, email='', password='', is_active=True)
            user.id = -1
            return user
        token_data = TokenData(login=login)
    except JWTError:
        raise credentials_exception()
    user = get_user_by_login(token_data.login, db)
    if user is None:
        raise credentials_exception()
    return user


async def get_current_active_user(token: str, db: Session):
    user = await get_current_user(token, db)
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user


async def get_anon_token():
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": ANON_LOGIN}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


async def authenticate(login: str, password: str, db: Session):
    user = get_user_by_login(login, db)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect login")
    if not verify_password(password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.login}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
