from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from .Associate import DBAssociate
from .Person import DBPerson


class DBVIP(DBPerson, DBAssociate):
    __tablename__ = "vips"

    id = Column(Integer, ForeignKey("person.id"), nullable=False, primary_key=True)
    timeslots = relationship("DBTimeslots", order_by="start_time.id", backref="vips")

    __mapper_args__ = {
        "polymorphic_identity": "vips",
    }
