import uuid

from fastapi import APIRouter, HTTPException, Depends
from pydantic import EmailStr
from sqlalchemy.orm import Session
from starlette.requests import Request

from database.starter import get_db
from helpers import dbtools
from helpers.hosttools import get_current_host
from models.Hosts import DBHost
from schemas import Attendee

registrationRouter = APIRouter()


# Main imports the reg router, so we import main after it
# TODO: Refactor the DBHost helpers in main somewhere else
# import main


@registrationRouter.post("/")
def signup(attendee: Attendee.Attendee, request: Request, db: Session = Depends(get_db)):
    # if things really hit the fan on deployment night, we can replay this from cloudwatch:
    print(f"Signup Request received | {attendee.json()}")
    if attendee.validattendee():
        if not dbtools.create_user(db, attendee, request.url_for):
            raise HTTPException(status_code=400, detail="Email is in use. Contact info@losaltoshacks.com if this is an error or to update your information.")
        raise HTTPException(status_code=200, detail="Ok")
    raise HTTPException(status_code=400, detail="Minors must provide guardian information. High school students must provide school and grade. Middle school students must provide school.")


@registrationRouter.get("/")
def list_users(db: Session = Depends(get_db), host: DBHost = Depends(get_current_host)):
    if host:
        if users := dbtools.get_users(db):
            return users
        return []
    raise HTTPException(status_code=401, detail="Unauthorized request.")


@registrationRouter.get("/{user_id}/")
def list_user(user_id: uuid.UUID, db: Session = Depends(get_db), host: DBHost = Depends(get_current_host)):
    if host:
        if user := dbtools.get_user(db, user_id):
            return user
        raise HTTPException(status_code=404, detail=f"USER <'{user_id.hex}'> not found.")
    raise HTTPException(status_code=401, detail="Unauthorized request.")


@registrationRouter.get("/{user_id}/history")
def list_users_history(user_id: uuid.UUID, db: Session = Depends(get_db),
                       host: DBHost = Depends(get_current_host)):
    if host:
        if user := dbtools.get_user(db, user_id, True):
            return user
        raise HTTPException(status_code=404, detail=f"USER <'{user_id.hex}'> not found.")
    raise HTTPException(status_code=401, detail="Unauthorized request.")


@registrationRouter.patch("/{user_id}/")
def update_user(user_id: uuid.UUID, data: dict, db: Session = Depends(get_db),
                host: DBHost = Depends(get_current_host)):
    if host:
        dbtools.update_user(db, user_id, data)
        raise HTTPException(status_code=200, detail=f"USER <'{user_id.hex}'> successfully updated.")
    raise HTTPException(status_code=401, detail="Unauthorized request.")


@registrationRouter.delete("/{user_id}/")
def delete_specified_user(user_id: uuid.UUID, db: Session = Depends(get_db),
                          host: DBHost = Depends(get_current_host)):
    if host:
        dbtools.update_user(db, user_id, {"outdated": True})
        raise HTTPException(status_code=200, detail=f"USER <'{user_id.hex}'> successfully deleted.")
    raise HTTPException(status_code=401, detail="Unauthorized request.")



# Do not remove it is used to figure out what parameters of a function are real
def is_valid(pair):
    if pair[1]:
        return pair


@registrationRouter.get("/search")
def search_for_specific(email: EmailStr = None,
                        db: Session = Depends(get_db), host: DBHost = Depends(get_current_host)):
    if host:
        if email:
            # meme = list(pair for pair in map(is_valid, locals().items()) if pair)[:-1]
            return dbtools.search_for_users(db, ("email", email))
        return HTTPException(status_code=404, detail="Invalid search request.")
    raise HTTPException(status_code=401, detail="Unauthorized request.")



