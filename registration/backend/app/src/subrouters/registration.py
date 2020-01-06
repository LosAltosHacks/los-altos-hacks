import uuid

import helpers.dbtools as dbtools
import schemas.Attendee as Attendee
from fastapi import APIRouter, HTTPException, Depends
from models.Hosts import DBHost
from pydantic import EmailStr
from sqlalchemy.orm import Session

registrationRouter = APIRouter()

# DONT TOUCH BELOW THIS FIXES A CIRCULAR IMPORT
import main  # NO TOUCHING LEFT THIS FIXES A CIRCULAR IMPORT


# DONT TOUCH ABOVE THIS FIXES A CIRCULAR IMPORT

@registrationRouter.post("/")
def signup(attendee: Attendee.Attendee, db: Session = Depends(main.get_db)):
    if attendee.validattendee():
        dbtools.create_user(db, attendee)
        raise HTTPException(status_code=200, detail="Ok")
    raise HTTPException(status_code=400, detail="Minors must provide guardian information.")


@registrationRouter.get("/")
def list_users(db: Session = Depends(main.get_db), host: DBHost = Depends(main.get_current_host)):
    if host:
        if users := dbtools.get_users(db):
            return users
        return []
    raise HTTPException(status_code=401, detail="Unauthorized request.")


@registrationRouter.get("/{user_id}/")
def list_user(user_id: uuid.UUID, db: Session = Depends(main.get_db), host: DBHost = Depends(main.get_current_host)):
    if host:
        if user := dbtools.get_user(db, user_id.hex):
            return user
        raise HTTPException(status_code=404, detail=f"USER <'{user_id.hex}'> not found.")
    raise HTTPException(status_code=401, detail="Unauthorized request.")


@registrationRouter.get("/{user_id}/history")
def list_users_history(user_id: uuid.UUID, db: Session = Depends(main.get_db),
                       host: DBHost = Depends(main.get_current_host)):
    if host:
        if user := dbtools.get_user(db, user_id.hex, True):
            return user
        raise HTTPException(status_code=404, detail=f"USER <'{user_id.hex}'> not found.")
    raise HTTPException(status_code=401, detail="Unauthorized request.")


@registrationRouter.patch("/{user_id}/")
def update_user(user_id: uuid.UUID, data: dict, db: Session = Depends(main.get_db),
                host: DBHost = Depends(main.get_current_host)):
    if host:
        dbtools.update_user(db, user_id.hex, data)
        raise HTTPException(status_code=200, detail=f"USER <'{user_id.hex}'> successfully updated.")
    raise HTTPException(status_code=401, detail="Unauthorized request.")


@registrationRouter.delete("/{user_id}/")
def delete_specified_user(user_id: uuid.UUID, db: Session = Depends(main.get_db),
                          host: DBHost = Depends(main.get_current_host)):
    if host:
        dbtools.update_user(db, user_id.hex, {"outdated": True})
        raise HTTPException(status_code=200, detail=f"USER <'{user_id.hex}'> successfully deleted.")
    raise HTTPException(status_code=401, detail="Unauthorized request.")


@registrationRouter.get("/verify/{user_id}/{email_token}/")
def verify_user(user_id: uuid.UUID, email_token: uuid.UUID, db: Session = Depends(main.get_db),
                host: DBHost = Depends(main.get_current_host)):
    if host:
        if user := dbtools.get_user(db, user_id.hex):
            if user.email_token == email_token and not user.email_verified:
                dbtools.update_user(db, user_id.hex, {"email_verified": True, "email_token": None})
                raise HTTPException(status_code=200, detail=f"USER <'{user_id.hex}'> has been verified!")
            raise HTTPException(status_code=304, detail=f"USER <'{user_id.hex}'> not modified.")
        raise HTTPException(status_code=404, detail=f"USER <'{user_id.hex}'> not found.")
    raise HTTPException(status_code=401, detail="Unauthorized request.")


# Do not remove it is used to figure out what parameters of a function are real
def is_valid(pair):
    if pair[1]:
        return pair


@registrationRouter.get("/search")
def search_for_specific(user_id: uuid.UUID = None, first_name: str = None, last_name: str = None,
                        email: EmailStr = None, phonenumber: str = None, guardian_first_name: str = None,
                        guardian_last_name: str = None, guardian_phone_number: str = None,
                        db: Session = Depends(main.get_db), host: DBHost = Depends(main.get_current_host)):
    if host:
        if user_id or first_name or last_name or email or phonenumber or guardian_first_name or guardian_last_name or guardian_phone_number:
            meme = list(pair for pair in map(is_valid, locals().items()) if pair)[:-1]
            return dbtools.search_for_users(db, meme)
        return list_users(db)
    raise HTTPException(status_code=401, detail="Unauthorized request.")
