import datetime
import uuid

from sqlalchemy import Column, String, Integer, Enum, Boolean, Date, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID

from ..database.starter import dbBase
from ..helpers.emailing import send_email_template
from ..schemas.Attendee import AcceptanceStatusEnum, ShirtSize, ProgrammingExperience


class DBPerson(dbBase):
    __tablename__ = "person2021"

    id = Column(Integer, primary_key=True)
    user_id = Column(UUID(as_uuid=True), nullable=False, default=uuid.uuid4)
    first_name = Column(String(256), nullable=False)
    last_name = Column(String(256), nullable=False)
    birthdate = Column(Date, nullable=False)
    gender = Column(String(256))
    ethnicity = Column(String(256))
    email = Column(String(256), nullable=False)
    email_token = Column(UUID(as_uuid=True), nullable=False, default=uuid.uuid4)
    email_verified = Column(Boolean, nullable=False, default=False)
    phone_number = Column(String(256))
    country = Column(Text, nullable=False)
    address_line_one = Column(Text, nullable=False)
    address_line_two = Column(Text)
    city = Column(Text, nullable=False)
    state_or_province = Column(Text)
    postal_code = Column(Text, nullable=False)
    twitter_handle = Column(String(256))
    github_username = Column(String(256))
    linkedin_profile = Column(String(256))
    programming_experience = Column(Enum(ProgrammingExperience), nullable=False)
    tshirt_size = Column(Enum(ShirtSize), nullable=False)
    acceptance_status = Column(Enum(AcceptanceStatusEnum), nullable=False, default=AcceptanceStatusEnum.none)
    outdated = Column(Boolean, nullable=False, default=False)
    timestamp = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)

    def send_verification_email(self, template, url_for):
        if self.email_verified:
            raise ValueError("User's email already verified.")
        full_name = self.first_name + " " + self.last_name
        print(_row2dict(self))
        full_data = {'email': self.email, 'first_name': self.first_name, 'verification_link': url_for("email_verify", user_id=self.user_id, email_token=self.email_token), 'full_name': full_name}
        send_email_template(full_data, template)

_row2dict = lambda r: {c.name: getattr(r, c.name) for c in DBPerson.__table__.columns}
