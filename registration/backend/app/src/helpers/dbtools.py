import datetime
import enum
from typing import Union

import database.starter as starter
import jwt
import schemas.Attendee as attendee
import schemas.Mentor as mentor
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from models.Attendee import DBAttendee
from models.Hosts import DBHost
from models.Mentor import DBMentor
from models.Person import DBPerson
from models.Timeslots import DBTimeslots
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette.status import HTTP_401_UNAUTHORIZED


def help_jsonify(x):
    if issubclass(type(x), enum.Enum):
        return x.value

    if type(x) is datetime.datetime:
        return str(x)

    return x


def get_user(db: Session, user_id: str, get_outdated: bool = False,
             model: Union[DBPerson, DBAttendee, DBMentor] = DBAttendee):
    query = db.query(model)
    if get_outdated:
        return query.filter(model.user_id == user_id).all()
    test = query.filter(model.user_id == user_id,
                        model.outdated != True).first()
    return test


def get_user_by_email(db: Session, email: str, get_outdated: bool = False,
                      model: Union[DBPerson, DBAttendee, DBMentor] = DBAttendee):
    query = db.query(model)
    if get_outdated:
        return query.filter(model.email == email).all()
    return query.filter(model.email == email,
                        model.outdated != (not get_outdated)).first()


def get_users(db: Session, skip: int = 0, limit: int = 100, model: Union[DBPerson, DBAttendee, DBMentor] = DBAttendee):
    return db.query(model).filter(model.outdated != True).offset(skip).limit(
        limit).all()


def create_user(db: Session, user: Union[attendee.Attendee, mentor.Mentor],
                url_for, model: Union[DBPerson, DBAttendee, DBMentor] = DBAttendee):
    # TODO: assert that model matches schema
    if model == DBMentor:
        db_user = DBMentor(
            first_name=user.first_name,
            last_name=user.last_name,
            over_18=user.over_18,
            company=user.company,
            email=user.email,
            phone_number=user.phone_number,
            tshirt_size=user.tshirt_size,
            skillset=user.skillset,
            dietary_restrictions=user.dietary_restrictions
        )
        for timeslot in user.timeslots:
            db_user.timeslots.append(
                DBTimeslots(start_time=datetime.datetime.strptime(timeslot.start_time, "%Y-%m-%dT%H:%M"),
                            end_time=datetime.datetime.strptime(timeslot.end_time, "%Y-%m-%dT%H:%M")))
    else:
        db_user = model(**dict(user))
    if get_user_by_email(db, user.email, model=model):
        # Disallow duplicate email registration
        return None
    db.add(db_user)
    # Fail commit if can't send email
    # But first, fill out auto fields with a flush:
    db.flush()
    db_user.send_verification_email("email_verify", url_for)
    db.commit()
    db.refresh(db_user)
    return db_user


def time_slot(db: Session, start_time: datetime, end_time: datetime, model: DBMentor = DBMentor):
    model.timeslots.append(DBTimeslots(start_time=start_time, end_time=end_time))
    db.commit()


def search_for_users(db: Session, criteria, model: Union[DBPerson, DBAttendee, DBMentor] = DBAttendee):
    query = db.query(model)
    for crit in criteria:
        query = query.filter(getattr(model, crit[0]) == crit[1])
    print("query", query)
    return query.all()


def update_user(db: Session, user_id: str, columns_to_update: dict,
                model: Union[DBPerson, DBAttendee, DBMentor] = DBAttendee):
    user = get_user(db, user_id, model=model)

    for key, value in columns_to_update.items():
        if hasattr(user, key):
            setattr(user, key, value)
    db.commit()


starter.dbBase.metadata.create_all(bind=starter.engine)
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

JWT_SECRET_KEY = ""


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


def create_access_token(*, data: dict, expires_delta: datetime.timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm="HS256")
    return encoded_jwt


async def get_current_host(db: Session = Depends(starter.get_db), token: str = Depends(oauth2_scheme)):
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
