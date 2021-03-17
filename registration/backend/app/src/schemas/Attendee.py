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
    school: str
    grade: int 
    phone_number: str
    country : str
    address_line_one : str
    address_line_two : str
    city : str
    state_or_province : str = None
    postal_code : str
    timezone : str
    birthdate : str
    gender : str
    ethnicity : str
    shirt_size : ShirtSize
    twitter_handle : str = None
    github_username : str = None
    linkedin_page_url : str = None
    parent_first_name : str = None
    parent_last_name : str = None
    parent_email : str = None
    parent_phone_number : str = None
    programming_experience : str = None
    previous_hackathons_attended : str = None
    hear_about_us : str = None
    access_to_laptop_or_tablet : str = None
    form_of_internet : str = None
    mlh_code_of_conduct : bool
    share_info_mlh : bool
    send_info_emails : bool = False

    class Config:
        orm_mode = True

    def hasinformation(self) -> bool:
        return bool(self.guardian_name and self.guardian_email and self.guardian_phone_number)

    def validattendee(self) -> bool:
        if self.age < 18 and not self.hasinformation():
            return False
        if self.education == "High School" and (not self.grade or not self.school):
            return False
        if self.education == "Middle School" and not self.school:
            return False
        return True
