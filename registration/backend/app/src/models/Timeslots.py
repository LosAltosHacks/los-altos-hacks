from database.starter import dbBase
from sqlalchemy import Column, Integer, DateTime, ForeignKey


class DBTimeslots(dbBase):
    __tablename__ = "timeslots"

    id = Column(Integer, nullable=False, primary_key=True)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    person_id = Column(Integer, ForeignKey("person.id"))

    __mapper_args__ = {
        "polymorphic_identity": "timeslots",
    }
