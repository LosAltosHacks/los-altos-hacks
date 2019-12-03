import uuid

import database.starter as starter
import helpers.dbtools as dbtools
import schemas.Attendee as attendee
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

starter.dbBase.metadata.create_all(bind=starter.engine)

# IS_JWTFORCED = os.getenv("JWTFORCED", "Y")

registrationRouter = APIRouter(redirect_slashes=False)


def get_db():
    try:
        db = starter.SessionLocal()
        yield db
    finally:
        db.close()


@registrationRouter.post("/signup/")
def signup(attendee: attendee.Attendee, db: Session = Depends(get_db)):
    if attendee.validattendee():
        dbtools.create_user(db, attendee)
        raise HTTPException(status_code=200, detail="Successfully processed attendee")
    raise HTTPException(status_code=400, detail="Minors must provide guardian information.")


@registrationRouter.get("/list/")
@registrationRouter.get("/list/{user_id}/")
def list_users(user_id: uuid.UUID = None, db: Session = Depends(get_db)):
    if user_id:
        if user := dbtools.get_user(db, user_id.hex):
            return user
        raise HTTPException(status_code=404, detail=f"USER <'{user_id.hex}'> not found.")
    return dbtools.get_users(db)


@registrationRouter.get("/history/{user_id}/")
def list_users_history(user_id: uuid.UUID, db: Session = Depends(get_db)):
    if user := dbtools.get_user(db, user_id.hex, True):
        return user
    raise HTTPException(status_code=404, detail=f"USER <'{user_id.hex}'> not found.")


@registrationRouter.patch("/list/{user_id}/")
def update_user(user_id: uuid.UUID, data: dict, db: Session = Depends(get_db)):
    dbtools.update_user(db, user_id.hex, data)
    raise HTTPException(status_code=200, detail=f"USER <'{user_id.hex}'> successfully updated.")


@registrationRouter.delete("/list/{user_id}/")
def delete_specified_user(user_id: uuid.UUID, db: Session = Depends(get_db)):
    dbtools.update_user(db, user_id.hex, {"outdated": True})
    raise HTTPException(status_code=200, detail=f"USER <'{user_id.hex}'> successfully deleted.")


@registrationRouter.get("/verify/{user_id}/{email_token}/")
def verify_user(user_id: uuid.UUID, email_token: uuid.UUID, db: Session = Depends(get_db)):
    if user := dbtools.get_user(db, user_id.hex):
        if user.email_token == email_token and not user.email_verified:
            dbtools.update_user(db, user_id.hex, {"email_verified": True})
            raise HTTPException(status_code=200, detail=f"USER <'{user_id.hex}'> has been verified!")
        raise HTTPException(status_code=304, detail=f"USER <'{user_id.hex}'> not modified.")
    raise HTTPException(status_code=404, detail=f"USER <'{user_id.hex}'> not found.")
