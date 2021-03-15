from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, Enum, Text
# from sqlalchemy.orm import relationship

from models.Person import DBPerson

import enum


class TechnologyProficiency(enum.Enum):
    beginner = "Beginner"
    intermediate = "Intermediate"
    advanced = "Advanced"


class DBMentor(DBPerson):
    __tablename__ = "mentors"

    id = Column(Integer, ForeignKey('person.id'), nullable=False, primary_key=True)
    occupation = Column(String(1024), nullable=False)
    technology_proficiency = Column(Enum(TechnologyProficiency), nullable=False)
    proficient_in_languages = Column(String(1024))
    specific_skills = Column(String(1024))

    __mapper_args__ = {
        "polymorphic_identity": "mentors"
    }
