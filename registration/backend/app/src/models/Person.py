import datetime
import uuid

from models.database import dbBase
from schemas.Attendee import AcceptanceStatusEnum, ShirtSize
from sqlalchemy import Column, String, Integer, Enum, Boolean, DateTime
from sqlalchemy.orm.session import object_session
from helpers.emailing import send_email_template
import helpers.dbtools as dbtools

class DBPerson(dbBase):
    __tablename__ = "person"

    id = Column(Integer, primary_key=True)
    user_id = Column(String(36), nullable=False, default=uuid.uuid4().hex)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    email_token = Column(String(36), nullable=False, default=uuid.uuid4().hex)
    email_verified = Column(Boolean, nullable=False, default=False)
    tshirt_size = Column(Enum(ShirtSize), nullable=False)
    dietary_restrictions = Column(String(255))
    acceptance_status = Column(Enum(AcceptanceStatusEnum), nullable=False, default=AcceptanceStatusEnum.none)
    signed_waiver = Column(Boolean, nullable=False, default=False)
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
