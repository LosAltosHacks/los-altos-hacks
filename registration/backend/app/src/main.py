from datetime import timedelta

import uvicorn
from database.starter import get_db
from fastapi import Depends, HTTPException
from fastapi import FastAPI
from fastapi.security import OAuth2PasswordRequestForm
from helpers.dbtools import authenticate_host, create_access_token, Token
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware
from starlette.status import HTTP_401_UNAUTHORIZED
from subrouters.mentors import mentorRouter
from subrouters.registration import registrationRouter

app = FastAPI(debug=True)

# TODO: Restrict origins
origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(registrationRouter, prefix="/attendees")
app.include_router(mentorRouter, prefix="/mentors")


@app.post("/token", response_model=Token)
async def login_host(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    if user := authenticate_host(db, form_data.username, form_data.password):
        access_token_expires = timedelta(minutes=30)
        access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
        return {"access_token": access_token, "token_type": "bearer"}
    raise HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )


if __name__ == '__main__':
    uvicorn.run(app, host="localhost", port=8000)
