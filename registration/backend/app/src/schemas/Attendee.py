import datetime
import enum
import math

import config
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


class ProgrammingExperience(enum.Enum):
    beginner = "Beginner"
    intermediate = "Intermediate"
    advanced = "Advanced"
    expert = "Expert"


class PreviousHackathons(enum.Enum):
    zero = "0"
    one = "1"
    two = "2"
    three = "3"
    four_plus = "4+"


class GradeLevel(enum.Enum):
    middle_school = "Middle School"
    ninth = "9th"
    tenth = "10th"
    eleventh = "11th"
    twelfth = "12th"
    college = "College"


class Attendee(BaseModel):
    first_name: str
    last_name: str
    birthdate: datetime.date  # YYYY-MM-DD
    email: EmailStr
    school: str
    grade: GradeLevel
    phone_number: str = None
    country: str
    address_line_one: str
    address_line_two: str = None
    city: str
    state_or_province: str
    postal_code: str
    gender: str
    ethnicity: str
    tshirt_size: ShirtSize
    twitter_handle: str = None
    github_username: str = None
    linkedin_profile: str = None
    parent_first_name: str = None
    parent_last_name: str = None
    parent_email: str = None
    parent_phone_number: str = None
    programming_experience: ProgrammingExperience
    previous_hackathons_attended: PreviousHackathons
    hear_about_us: str = None
    access_to_laptop_or_tablet: bool = None
    form_of_internet: str = None
    mlh_code_of_conduct: bool
    share_info_mlh: bool
    send_info_emails: bool = None
    share_info_lah: bool

    class Config:
        orm_mode = True

    def hasinformation(self) -> bool:
        return bool(self.parent_first_name and self.parent_last_name and self.parent_email)

    def validattendee(self) -> bool:
        age = math.floor((datetime.date.fromisoformat(config.HACKATHON_DATE) - self.birthdate).days / 365)
        if age < 18 and not self.hasinformation():
            return False
        if self.grade.value in ("9th", "10th", "11th", "12th") and (not self.grade or not self.school):
            return False
        if self.grade.value == "Middle School" and not self.school:
            return False
        return True
