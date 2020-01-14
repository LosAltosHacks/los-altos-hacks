import datetime
import enum
from typing import Union

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
                url_for, model: Union[DBPerson, DBAttendee, DBMentor] = DBAttendee):
    # TODO: assert that model matches schema
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


def search_for_users(db: Session, criteria, model: Union[DBPerson, DBAttendee, DBMentor] = DBAttendee):
    query = db.query(model)
    for crit in criteria:
        query = query.filter(getattr(model, crit[0]) == crit[1])
    return query.all()


def update_user(db: Session, user_id: str, columns_to_update: dict,
                model: Union[DBPerson, DBAttendee, DBMentor] = DBAttendee):
    user = get_user(db, user_id, model=model)

    for key, value in columns_to_update.items():
        if hasattr(user, key):
            setattr(user, key, value)
        else:
            raise KeyError(f"Model {model} has no attribute {key}")
    db.commit()
