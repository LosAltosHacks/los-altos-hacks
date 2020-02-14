from fastapi import APIRouter, HTTPException, Depends
from models.Hosts import DBHost
from models.Person import DBPerson
from models.Mentor import DBMentor
from models.Judge import DBJudge
from models.Sponsor import DBSponsor
from models.Chaperone import DBChaperone
from models.VIP import DBVIP
from models.database import get_db
from sqlalchemy.orm import Session
from pydantic import EmailStr
from starlette.requests import Request
from starlette.responses import Response

verificationRouter = APIRouter()

@verificationRouter.get("/get/{email}")
def get_user_by_email(email: EmailStr, request: Request, db: Session = Depends(get_db)):
	query = db.query(DBPerson)
	person = query.filter(DBPerson.email == email).first()
	for model in [DBJudge, DBChaperone, DBVIP, DBSponsor, DBMentor, DBPerson]:
		role = model # How do I get a string name of the model? can I use model.__tablename__ ?
		matching = db.query(model).filter(model.email == email)
		if matching.exists():
			return role, person