from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Text, Enum

from models.Person import DBPerson
from schemas.Attendee import PreviousHackathons, GradeLevel


class DBAttendee(DBPerson):
    __tablename__ = "attendees2021"

    id = Column(Integer, ForeignKey('person2021.id'), nullable=False, primary_key=True)

    # education = Column(String(256), nullable=False)
    school = Column(String(256))
    grade = Column(Enum(GradeLevel), nullable=False)
    parent_first_name = Column(String(256))
    parent_last_name = Column(String(256))
    parent_email = Column(String(256))
    parent_phone_number = Column(String(256))
    previous_hackathons_attended = Column(Enum(PreviousHackathons), nullable=False)
    hear_about_us = Column(Text, nullable=False)
    access_to_laptop_or_tablet = Column(Boolean, nullable=False)
    form_of_internet = Column(Text, nullable=False)
    mlh_code_of_conduct = Column(Boolean, nullable=False)
    share_info_mlh = Column(Boolean, nullable=False)
    share_info_lah = Column(Boolean, nullable=False)
    send_info_emails = Column(Boolean)

    __mapper_args__ = {
        "polymorphic_identity": "attendees",
    }
