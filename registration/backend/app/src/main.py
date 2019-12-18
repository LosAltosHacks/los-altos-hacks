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

if __name__ == '__main__':
    uvicorn.run(app, host="localhost", port=8000)
