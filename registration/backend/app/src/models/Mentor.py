from sqlalchemy import Column, String, Boolean, Integer, ForeignKey

from .Person import DBPerson


class DBMentor(DBPerson):
    __tablename__ = "mentor"

    id = Column(Integer, ForeignKey('person.id'), nullable=False, primary_key=True)
    over_18 = Column(Boolean, nullable=False)
    skillset = Column(String(1000))

    __mapper_args__ = {
        "polymorphic_identity": "mentor"
    }
