import datetime
import enum
from typing import Union, Dict

import schemas.Attendee as attendee
import schemas.Mentor as mentor
from models.Attendee import DBAttendee
from models.Mentor import DBMentor
from models.Person import DBPerson
from sqlalchemy.orm import Session


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
                model: Union[DBPerson, DBAttendee, DBMentor] = DBAttendee):
    db_user = model(**dict(user))
    if olduser := get_user_by_email(db, user.email, model=model):
        db_user.user_id = olduser.user_id
        olduser.outdated = True
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def search_for_users(db: Session, criteria: Dict[str, str]):
    return db.query(DBPerson).filter_by(**criteria).all()


def update_user(db: Session, user_id: str, columns_to_update: dict,
                model: Union[DBPerson, DBAttendee, DBMentor] = DBAttendee):
    user = get_user(db, user_id, model=model)

    for key, value in columns_to_update.items():
        if hasattr(user, key):
            setattr(user, key, value)
    db.commit()

# def add_timeslot(db: Session, user: DBPerson):
#     DBTimeslots(start_time=datetime.datetime.utcnow(), end_time=datetime.datetime.utcnow(), mentor=user)
#     db.commit()
