import os
import uvicorn
from fastapi import FastAPI
from subrouters.registration import registrationRouter
from starlette.middleware.cors import CORSMiddleware

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

app.config = {}
app.config['SQLALCHEMY_DATABASE_URL'] = os.getenv('SQLALCHEMY_DATABASE_URL')
app.config['SES_AWS_REGION'] = os.getenv('SES_AWS_REGION')
app.config['SES_SENDER'] = os.getenv('SES_SENDER')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

if __name__ == '__main__':
    uvicorn.run(app, host="localhost", port=8000)
