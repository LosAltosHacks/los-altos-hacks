from models.Person import DBPerson
from sqlalchemy import Column, String, Integer, ForeignKey


class DBAssociate(DBPerson):
    __tablename__ = "associates"

    id = Column(Integer, ForeignKey("person.id"), nullable=False, primary_key=True)
    company = Column(String(1000), nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "associates",
    }
