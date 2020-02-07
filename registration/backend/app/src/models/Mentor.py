from sqlalchemy import Column, String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import relationship

from .Associate import DBAssociate


class DBMentor(DBAssociate):
    __tablename__ = "mentors"

    id = Column(Integer, ForeignKey('associates.id'), nullable=False, primary_key=True)
    over_18 = Column(Boolean, nullable=False)
    phone_number = Column(String(255), nullable=False)
    skillset = Column(String(1000))
    timeslots = relationship("DBTimeslots", backref="mentor", order_by="DBTimeslots.start_time", lazy='selectin')

    __mapper_args__ = {
        "polymorphic_identity": "mentors"
    }