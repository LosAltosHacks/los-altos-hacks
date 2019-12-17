import uuid

import database.starter as starter
import helpers.dbtools as dbtools
import schemas.Attendee as Attendee
from fastapi import APIRouter, HTTPException, Depends
from pydantic import EmailStr
from sqlalchemy.orm import Session

starter.dbBase.metadata.create_all(bind=starter.engine)

# IS_JWTFORCED = os.getenv("JWTFORCED", "Y")

registrationRouter = APIRouter()


def get_db():
    try:
        db = starter.SessionLocal()
        yield db
    finally:
        db.close()


@registrationRouter.post("/")
def signup(attendee: Attendee.Attendee, db: Session = Depends(get_db)):
    if attendee.validattendee():
        dbtools.create_user(db, attendee)
        raise HTTPException(status_code=200, detail="Ok")
    raise HTTPException(status_code=400, detail="Minors must provide guardian information.")


@registrationRouter.get("/")
def list_users(db: Session = Depends(get_db)):
    if users := dbtools.get_users(db):
        return users
    return []


@registrationRouter.get("/{user_id}/")
def list_user(user_id: uuid.UUID, db: Session = Depends(get_db)):
    if user := dbtools.get_user(db, user_id.hex):
        return user
    raise HTTPException(status_code=404, detail=f"USER <'{user_id.hex}'> not found.")


@registrationRouter.get("/{user_id}/history")
def list_users_history(user_id: uuid.UUID, db: Session = Depends(get_db)):
    if user := dbtools.get_user(db, user_id.hex, True):
        return user
    raise HTTPException(status_code=404, detail=f"USER <'{user_id.hex}'> not found.")


@registrationRouter.patch("/{user_id}/")
def update_user(user_id: uuid.UUID, data: dict, db: Session = Depends(get_db)):
    dbtools.update_user(db, user_id.hex, data)
    raise HTTPException(status_code=200, detail=f"USER <'{user_id.hex}'> successfully updated.")


@registrationRouter.delete("/{user_id}/")
def delete_specified_user(user_id: uuid.UUID, db: Session = Depends(get_db)):
    dbtools.update_user(db, user_id.hex, {"outdated": True})
    raise HTTPException(status_code=200, detail=f"USER <'{user_id.hex}'> successfully deleted.")


@registrationRouter.get("/verify/{user_id}/{email_token}/")
def verify_user(user_id: uuid.UUID, email_token: uuid.UUID, db: Session = Depends(get_db)):
    if user := dbtools.get_user(db, user_id.hex):
        if user.email_token == email_token and not user.email_verified:
            dbtools.update_user(db, user_id.hex, {"email_verified": True, "email_token": None})
            raise HTTPException(status_code=200, detail=f"USER <'{user_id.hex}'> has been verified!")
        raise HTTPException(status_code=304, detail=f"USER <'{user_id.hex}'> not modified.")
    raise HTTPException(status_code=404, detail=f"USER <'{user_id.hex}'> not found.")


# @registrationRouter.post("/mentortest/")
# def make_mentor(mentor: Mentor.Mentor, db: Session = Depends(get_db)):
#     dbtools.create_user(db, mentor, dbMentor.DBMentor)
#     raise HTTPException(status_code=200, detail="OK")
#
#
# @registrationRouter.get("/mentortimeslots/{user_id}/")
# def timeslots(user_id: uuid.UUID, db: Session = Depends(get_db)):
#     if user := dbtools.get_user(db, user_id.hex, model=dbMentor.DBMentor):
#         dbtools.add_timeslot(db, user)
#         raise HTTPException(status_code=200, detail="Added timeslot")
#     raise HTTPException(status_code=404, detail=f"User <'{user_id.hex}'> not found.")
#
#
# @registrationRouter.get("/mentortest/{user_id}/")
# def get_mentor(user_id: uuid.UUID, db: Session = Depends(get_db)):
#     if user := dbtools.get_user(db, user_id.hex, model=dbMentor.DBMentor):
#         return user
#     raise HTTPException(status_code=404, detail=f"User <'{user_id.hex}'> not found.")


@registrationRouter.get("/search")
def search_for_specific(user_id: uuid.UUID = None, first_name: str = None, last_name: str = None,
                        email: EmailStr = None, phonenumber: str = None, guardian_first_name: str = None,
                        guardian_last_name: str = None, guardian_phone_number: str = None,
                        db: Session = Depends(get_db)):
    if user_id or first_name or last_name or email or phonenumber or guardian_first_name or guardian_last_name or guardian_phone_number:
        pass  # TODO: Finish db search endpoint
