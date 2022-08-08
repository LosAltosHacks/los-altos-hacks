import datetime
import enum
import uuid
from typing import Union

from sqlalchemy.orm import Session
from sqlalchemy import func

from models.Attendee import DBAttendee
from models.Mentor import DBMentor
from models.Person import DBPerson

import schemas.Mentor as mentor
import schemas.Attendee as attendee


def help_jsonify(x):
    if issubclass(type(x), enum.Enum):
        return x.value

    if type(x) is datetime.datetime:
        return str(x)

    return x


def get_user(db: Session, user_id: uuid.UUID, get_outdated: bool = False,
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
                        model.outdated != True).first()


def get_users(db: Session, skip: int = 0, limit: int = 1000, model: Union[DBPerson, DBAttendee, DBMentor] = DBAttendee):
    return db.query(model).filter(model.outdated != True).offset(skip).limit(
        limit).all()


def create_user(db: Session, user: Union[mentor.Mentor, attendee.Attendee],
                url_for, model: Union[DBMentor, DBAttendee] = DBAttendee):
    db_user = None
    if model is DBAttendee:
        db_user = DBAttendee(
            first_name=user.first_name,
            last_name=user.last_name,
            birthdate=user.birthdate,
            email=user.email,
            school=user.school,
            grade=user.grade,
            phone_number=user.phone_number,
            country=user.country,
            address_line_one=user.address_line_one,
            address_line_two=user.address_line_two,
            city=user.city,
            state_or_province=user.state_or_province,
            postal_code=user.postal_code,
            gender=user.gender,
            ethnicity=user.ethnicity,
            tshirt_size=user.tshirt_size,
            twitter_handle=user.twitter_handle,
            github_username=user.github_username,
            linkedin_profile=user.linkedin_profile,
            parent_first_name=user.parent_first_name,
            parent_last_name=user.parent_last_name,
            parent_email=user.parent_email,
            parent_phone_number=user.parent_phone_number,
            programming_experience=user.programming_experience,
            previous_hackathons_attended=user.previous_hackathons_attended,
            hear_about_us=user.hear_about_us,
            access_to_laptop_or_tablet=user.access_to_laptop_or_tablet,
            form_of_internet=user.form_of_internet,
            mlh_code_of_conduct=user.mlh_code_of_conduct,
            share_info_mlh=user.share_info_mlh,
            send_info_emails=user.send_info_emails,
            share_info_lah=user.share_info_lah
        )
    elif model is DBMentor:
        db_user = DBMentor(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            phone_number=user.phone_number,
            occupation=user.occupation,
            country=user.country,
            address_line_one=user.address_line_one,
            address_line_two=user.address_line_two,
            city=user.city,
            state_or_province=user.state_or_province,
            postal_code=user.postal_code,
            birthdate=user.birthdate,
            gender=user.gender,
            ethnicity=user.ethnicity,
            tshirt_size=user.tshirt_size,
            twitter_handle=user.twitter_handle,
            github_username=user.github_username,
            linkedin_profile=user.linkedin_profile,
            programming_experience=user.programming_experience,
            technology_proficiency=user.technology_proficiency,
            proficient_in_languages=user.proficient_in_languages,
            specific_skills=user.specific_skills
        )
    if not db_user:
        return None
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
    query = query.filter(func.lower(getattr(model, criteria[0])) == func.lower(criteria[1]))
    return query.all()


def update_user(db: Session, user_id: uuid.UUID, columns_to_update: dict,
                model: Union[DBPerson, DBAttendee, DBMentor] = DBAttendee):
    user = get_user(db, user_id, model=model)

    for key, value in columns_to_update.items():
        if hasattr(user, key):
            setattr(user, key, value)
        else:
            raise KeyError(f"Model {model} has no attribute {key}")
    db.commit()
