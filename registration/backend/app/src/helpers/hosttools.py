from datetime import datetime, timedelta

import config
import jwt
from fastapi import HTTPException, Depends, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette.status import HTTP_401_UNAUTHORIZED

from database.starter import get_db
from models.Hosts import DBHost

JWT_SECRET_KEY = config.JWT_SECRET_KEY

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

authRouter = APIRouter()


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str = None


class Host(BaseModel):
    email: str
    password: str
    disabled: bool


def is_host_password(password, hashed):
    return password_context.verify(password, hashed)


def create_password_hash(password):
    return password_context.hash(password)


def get_host_password(db: Session, email: str) -> DBHost:
    if user := db.query(DBHost).filter(DBHost.email == email).scalar():
        return user


def authenticate_host(db: Session, email: str, password: str):
    if hostpw := get_host_password(db, email):
        if not is_host_password(password, hostpw.password):
            return False
        return hostpw
    return False


def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm="HS256")
    return encoded_jwt


async def get_current_host(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except jwt.PyJWTError:
        raise credentials_exception
    user = db.query(DBHost).filter(DBHost.email == token_data.email).scalar()
    if user is None:
        raise credentials_exception
    return user


@authRouter.post("/token", response_model=Token)
async def login_host(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    if user := authenticate_host(db, form_data.username, form_data.password):
        access_token_expires = timedelta(minutes=30)
        access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
        return {"access_token": access_token, "token_type": "bearer"}
    raise HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
