import enum

from models.database import get_db
# from helpers.dbtools import get_users
import helpers.dbtools as dbtools
from pydantic import BaseModel, EmailStr


class AcceptanceStatusEnum(enum.Enum):
    none = "none"
    waitlist_queue = "waitlist_queue"
    waitlisted = "waitlisted"
    rejected = "rejected"
    queue = "queue"
    accepted = "accepted"

class ShirtSize(enum.Enum):
    small = "S"
    medium = "M"
    large = "L"
    extraLarge = "XL"

class Attendee(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    age: int
    education: str
    school: str = None
    grade: int = None
    phone_number: str
    gender: str = None
    ethnicity: str = None
    tshirt_size: ShirtSize
    previous_hackathons: int
    guardian_name: str = None
    guardian_email: EmailStr = None
    guardian_phone_number: str = None
    github_username: str = None
    linkedin_profile: str = None
    dietary_restrictions: str = None
    goals: str = None
    special: str = None

    class Config:
        orm_mode = True

    def hasinformation(self) -> bool:
        return bool(self.guardian_name and self.guardian_email and self.guardian_phone_number)

    def validattendee(self) -> bool:
        if not (self.age >= 18 or self.age < 18 and self.hasinformation()):
            return False
        if self.education == "High School":
            return self.grade and self.school
