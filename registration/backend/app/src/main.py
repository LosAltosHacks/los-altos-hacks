# Fail dynamic config early
from sqlalchemy.orm import Session

import config
import uvicorn
from fastapi import FastAPI
import models.database
from starlette.middleware.cors import CORSMiddleware
from subrouters.registration import registrationRouter

app = FastAPI()

origins = [
    "https://losaltoshacks.com",
    "https://www.losaltoshacks.com",
]
if config.is_development_env():
    origins.append("*")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)
app.include_router(registrationRouter, prefix="/attendees")


@app.get("/health/")
def health_check():
    return {"health": "good"}


# TODO: find out why this 401s when on the registrationRouter
@app.get("/nces_school_search/")
def query_schools(state: str = "", city: str = "", zipcode: str = "", name: str = ""):
    import requests
    r = requests.get(
        "https://nces.ed.gov/globallocator/index.asp?State={}&city={}&zipcode={}&miles=&itemname={"
        "}&sortby=name&School=1&PrivSchool=1".format(
            state, city, zipcode, name))
    print(r)
    return r.content


if __name__ == '__main__':
    models.database.do_create_all()
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info", proxy_headers=True)
