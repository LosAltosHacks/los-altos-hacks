import datetime
import uuid

from database.starter import dbBase
from schemas.Attendee import AcceptanceStatusEnum, ShirtSize
from sqlalchemy import Column, String, Integer, Enum, Boolean, DateTime


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