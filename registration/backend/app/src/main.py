# Fail dynamic config early
import config
import os
from datetime import datetime, timedelta

import jwt
import uvicorn
from fastapi import Depends, HTTPException
from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import models.database
from models.database import get_db
from models.Hosts import DBHost
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware
from starlette.status import HTTP_401_UNAUTHORIZED
from subrouters.registration import registrationRouter

app = FastAPI()

origins = [
    "losaltoshacks.com",
    "www.losaltoshacks.com",
]
if config.is_development_env():
    origins.append("*")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)
app.include_router(registrationRouter, prefix="/attendees")
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

@app.get("/health/")
def health_check():
    return {"health": "good"}

# TODO: find out why this 401s when on the registrationRouter
@app.get("/nces_school_search/")
def query_schools(state: str = "", city: str = "", zipcode: str = "", name: str = ""):
    import requests
    r = requests.get("https://nces.ed.gov/globallocator/index.asp?State={}&city={}&zipcode={}&miles=&itemname={}&sortby=name&School=1&PrivSchool=1".format(state, city, zipcode, name))
    print(r)
    return r.content


# TODO: remove this constant
JWT_SECRET_KEY = config.JWT_SECRET_KEY


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


@app.post("/token", response_model=Token)
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


if __name__ == '__main__':
    models.database.do_create_all()
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info", proxy_headers=True)
