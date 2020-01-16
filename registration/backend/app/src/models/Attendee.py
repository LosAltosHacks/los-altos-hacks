from sqlalchemy import Column, String, SmallInteger, Integer, ForeignKey

from .Person import DBPerson


class DBAttendee(DBPerson):
    __tablename__ = "attendees"

    id = Column(Integer, ForeignKey('person.id'), nullable=False, primary_key=True)
    age = Column(SmallInteger, nullable=False)

    education = Column(String(255), nullable=False)
    school = Column(String(255))
    grade = Column(SmallInteger)
    phone_number = Column(String(255), nullable=False)
    guardian_name = Column(String(255))
    guardian_email = Column(String(255))
    guardian_phone_number = Column(String(255))
    gender = Column(String(255))
    ethnicity = Column(String(255))
    previous_hackathons = Column(SmallInteger, nullable=False)
    github_username = Column(String(255))
    linkedin_profile = Column(String(255))
    goals = Column(String(1000))
    special = Column(String(1000))

    __mapper_args__ = {
        "polymorphic_identity": "attendees",
    }