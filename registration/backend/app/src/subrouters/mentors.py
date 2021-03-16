import uuid
import datetime
from typing import List

import schemas.Mentor as Mentor
from fastapi import APIRouter, HTTPException, Depends

import schemas.Attendee as Attendee
from models.Hosts import DBHost
from models.Mentor import DBMentor
from database.starter import get_db
import helpers.dbtools as dbtools
from pydantic import EmailStr, BaseModel
from sqlalchemy.orm import Session
from starlette.requests import Request
# from starlette.responses import Response

from helpers.hosttools import get_current_host
# import main

mentorRouter = APIRouter()


# class MentorData(BaseModel):
#     last_name: str
#     over_18: bool
#     user_id: str
#     signed_waiver: bool
#     dietary_restrictions: str
#     email_verified: bool
#     email: str
#     first_name: str
#     phone_number: str
#     company: str
#     outdated: bool
#     acceptance_status: Attendee.AcceptanceStatusEnum
#     tshirt_size: Attendee.ShirtSize
#
#     class Config:
#         orm_mode = True


@mentorRouter.post("/")
def signup(mentor: Mentor.Mentor, request: Request, db: Session = Depends(get_db)):
    # if things really hit the fan on deployment night, we can replay this from cloudwatch:
    print(f"Signup Request received | {mentor.json()}")
    if not dbtools.create_user(db, mentor, request.url_for, model=DBMentor):
        raise HTTPException(status_code=400, detail="Email is in use. Contact info@losaltoshacks.com if this is an error or to update your information.")
    raise HTTPException(status_code=200, detail="Ok")


@mentorRouter.get("/")
def list_users(db: Session = Depends(get_db), host: DBHost = Depends(get_current_host)):
    if host:
        if users := dbtools.get_users(db, model=DBMentor):
            return users
        return []
    raise HTTPException(status_code=401, detail="Unauthorized request.")


@mentorRouter.get("/{user_id}/")
def list_user(user_id: uuid.UUID, db: Session = Depends(get_db), host: DBHost = Depends(get_current_host)):
    if host:
        if user := dbtools.get_user(db, user_id, model=DBMentor):
            return user
        raise HTTPException(status_code=404, detail=f"USER <'{user_id.hex}'> not found.")
    raise HTTPException(status_code=401, detail="Unauthorized request.")


@mentorRouter.get("/{user_id}/history")
def list_users_history(user_id: uuid.UUID, db: Session = Depends(get_db),
                       host: DBHost = Depends(get_current_host)):
    if host:
        if user := dbtools.get_user(db, user_id, True, model=DBMentor):
            return user
        raise HTTPException(status_code=404, detail=f"USER <'{user_id.hex}'> not found.")
    raise HTTPException(status_code=401, detail="Unauthorized request.")


@mentorRouter.patch("/{user_id}/")
def update_user(user_id: uuid.UUID, data: dict, db: Session = Depends(get_db),
                host: DBHost = Depends(get_current_host)):
    if host:
        dbtools.update_user(db, user_id, data, model=DBMentor)
        raise HTTPException(status_code=200, detail=f"USER <'{user_id.hex}'> successfully updated.")
    raise HTTPException(status_code=401, detail="Unauthorized request.")


@mentorRouter.delete("/{user_id}/")
def delete_specified_user(user_id: uuid.UUID, db: Session = Depends(get_db),
                          host: DBHost = Depends(get_current_host)):
    if host:
        dbtools.update_user(db, user_id, {"outdated": True}, model=DBMentor)
        raise HTTPException(status_code=200, detail=f"USER <'{user_id.hex}'> successfully deleted.")
    raise HTTPException(status_code=401, detail="Unauthorized request.")


# @mentorRouter.get("/verify/{user_id}/{email_token}/", name="email_verify_mentor")
# def verify_user(user_id: uuid.UUID, email_token: uuid.UUID, db: Session = Depends(get_db)):
#
#     def mk_response(code, msg):
#         return Response(status_code=code, content=EMAIL_VERIFIED_PAGE_TEMPLATE.format(message=msg), media_type="text/html")
#
#     if not (user := dbtools.get_user(db, user_id)):
#         return mk_response(400, "User not found. How did you get here?")
#     if user.email_verified:
#         return mk_response(400, "Your email is already verified. You're good to go!")
#     if not user.email_token == email_token:
#         return mk_response(400, "Invalid token. Trying to cheat? :0")
#
#     dbtools.update_user(db, user_id, {"email_verified": True}, model=DBMentor)
#     return mk_response(200, "Email successfully verified. All done!")


# Do not remove it is used to figure out what parameters of a function are real
def is_valid(pair):
    if type(pair[1]) is str:
        return pair


@mentorRouter.get("/search")
def search_for_specific(email: EmailStr = None,
                        db: Session = Depends(get_db), host: DBHost = Depends(get_current_host)):
    if host:
        if email:
            # meme = list(pair for pair in map(is_valid, locals().items()) if pair)
            return dbtools.search_for_users(db=db, criteria=("email", email), model=DBMentor)
        return list_users(db)
    raise HTTPException(status_code=401, detail="Unauthorized request.")

# EMAIL_VERIFIED_PAGE_TEMPLATE = """
# <!DOCTYPE html>
# <html>
#   <head>
#     <title>Email Verification</title>
#     <meta charset="utf-8" />
#     <meta
#       name="viewport"
#       content="width=device-width, initial-scale=1, viewport-fit=cover"
#     />
#     <meta name="robots" content="noindex" />
#
#     <link rel="shortcut icon" href="https://www.losaltoshacks.com/favicon.ico" />
#     <link rel="icon" type="image/png" href="https://www.losaltoshacks.com/favicon.png" />
#     <link rel="apple-touch-icon" href="https://www.losaltoshacks.com/touch-icon.png" />
#
#     <link rel="stylesheet" type="text/css" href="https://www.losaltoshacks.com/css/reset.css" />
#     <link rel="stylesheet" type="text/css" href="https://www.losaltoshacks.com/css/fonts.css" />
#     <link rel="stylesheet" type="text/css" href="https://www.losaltoshacks.com/css/error.css" />
#   </head>
#   <body>
#     <article>
#       <div class="container">
#         <img id="logo" src="https://www.losaltoshacks.com/images/lahv-logo-vector.svg" />
#         <h1>{message}</h1>
#         <p>
#           Feel free to close the page or
#           <a href="https://losaltoshacks.com">return to the main website</a>.
#           For any kind of help, please contact us at
#           <a href="mailto:info@losaltoshacks.com">info@losaltoshacks.com</a>.
#         </p>
#       </div>
#     </article>
#   </body>
# </html>
# """