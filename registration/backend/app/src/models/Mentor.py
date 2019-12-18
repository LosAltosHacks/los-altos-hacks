from sqlalchemy import Column, String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import relationship

from .Person import DBPerson


class DBMentor(DBPerson):
    __tablename__ = "mentors"

    id = Column(Integer, ForeignKey('person.id'), nullable=False, primary_key=True)
    over_18 = Column(Boolean, nullable=False)
    skillset = Column(String(1000))
    # timeslots = relationship("DBTimeslots", backref="mentor", order_by="DBTimeslots.start_time", lazy='selectin')

    __mapper_args__ = {
        "polymorphic_identity": "mentors"
    }
