import enum

from sqlalchemy import Column, String, Integer, ForeignKey, Enum

from models.Person import DBPerson


# from sqlalchemy.orm import relationship


class TechnologyProficiency(enum.Enum):
    beginner = "Beginner"
    intermediate = "Intermediate"
    advanced = "Advanced"


class DBMentor(DBPerson):
    __tablename__ = "mentors2022"

    id = Column(Integer, ForeignKey('person2021.id'), nullable=False, primary_key=True)
    occupation = Column(String(1024), nullable=False)
    technology_proficiency = Column(Enum(TechnologyProficiency), nullable=False)
    proficient_in_languages = Column(String(1024))
    specific_skills = Column(String(1024))

    __mapper_args__ = {
        "polymorphic_identity": "mentors"
    }
