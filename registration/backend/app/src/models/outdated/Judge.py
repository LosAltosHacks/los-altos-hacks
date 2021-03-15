from sqlalchemy import Column, Integer, ForeignKey

from .Associate import DBAssociate
from Person import DBPerson
from .Positioned import DBPositioned


class DBJudge(DBPerson, DBAssociate, DBPositioned):
    __tablename__ = "judges"

    id = Column(Integer, ForeignKey("person.id"), nullable=False, primary_key=True)

    __mapper_args__ = {
        "polymorphic_identity": "judges",
    }
