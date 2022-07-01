# Fail dynamic config early
import uuid

import uvicorn
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import Response

import config
import database.starter
import helpers.dbtools as dbtools
from database.starter import get_db
from helpers.hosttools import authRouter
from models.Person import DBPerson
from subrouters.registration import registrationRouter

def create_app() -> CORSMiddleware:
    """Create app wrapper to overcome middleware issues."""

    origins = [
        "https://losaltoshacks.com",
        "https://www.losaltoshacks.com",
    ]

    if config.is_development_env():
        origins.append("*")

    fastapi_app = FastAPI()
    app.include_router(registrationRouter, prefix="/attendees")
    # app.include_router(mentorRouter, prefix="/mentors")
    app.include_router(authRouter, prefix="/auth")
    return CORSMiddleware(
        fastapi_app,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["POST", "GET"],
        allow_headers=["*"],
    )


app = create_app()

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


@app.get("/verify/{user_id}/{email_token}/", name="email_verify")
def verify_user(user_id: uuid.UUID, email_token: uuid.UUID, db: Session = Depends(get_db)):

    def mk_response(code, msg):
        return Response(status_code=code, content=EMAIL_VERIFIED_PAGE_TEMPLATE.format(message=msg), media_type="text/html")

    if not (user := dbtools.get_user(db, user_id, model=DBPerson)):
        return mk_response(400, "User not found. How did you get here?")
    if user.email_verified:
        return mk_response(400, "Your email is already verified. You're good to go!")
    if not user.email_token == email_token:
        return mk_response(400, "Invalid token. Trying to cheat? :0")

    dbtools.update_user(db, user_id, {"email_verified": True}, model=DBPerson)
    return mk_response(200, "Email successfully verified. All done!")


# TODO clean this up, brittleness on main site and uncleanly location:
EMAIL_VERIFIED_PAGE_TEMPLATE = """
<!DOCTYPE html>
<html>
  <head>
    <title>Email Verification</title>
    <meta charset="utf-8" />
    <meta
      name="viewport"
      content="width=device-width, initial-scale=1, viewport-fit=cover"
    />
    <meta name="robots" content="noindex" />

    <link rel="shortcut icon" href="https://www.losaltoshacks.com/favicon.ico" />
    <link rel="icon" type="image/png" href="https://www.losaltoshacks.com/favicon.png" />
    <link rel="apple-touch-icon" href="https://www.losaltoshacks.com/touch-icon.png" />

    <link rel="stylesheet" type="text/css" href="https://www.losaltoshacks.com/css/reset.css" />
    <link rel="stylesheet" type="text/css" href="https://www.losaltoshacks.com/css/fonts.css" />
    <link rel="stylesheet" type="text/css" href="https://www.losaltoshacks.com/css/error.css" />
  </head>
  <body>
    <article>
      <div class="container">
        <img id="logo" src="https://www.losaltoshacks.com/images/lahv-logo-vector.svg" />
        <h1>{message}</h1>
        <p>
          Feel free to close the page or
          <a href="https://losaltoshacks.com">return to the main website</a>.
          For any kind of help, please contact us at
          <a href="mailto:info@losaltoshacks.com">info@losaltoshacks.com</a>.
        </p>
      </div>
    </article>
  </body>
</html>
"""


if __name__ == '__main__':
    database.starter.do_create_all()
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info", proxy_headers=True)
