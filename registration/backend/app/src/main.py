import uvicorn
from fastapi import FastAPI
from subrouters.registration import registrationRouter

app = FastAPI(debug=True)

app.include_router(registrationRouter, prefix="/attendees")

if __name__ == '__main__':
    uvicorn.run(app, host="localhost", port=8000)
