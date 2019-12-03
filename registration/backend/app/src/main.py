from fastapi import FastAPI
from subrouters.registration import registrationRouter

app = FastAPI(debug=True)

app.include_router(registrationRouter, prefix="/registration/v1")
