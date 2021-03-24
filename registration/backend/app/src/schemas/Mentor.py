import datetime

from pydantic import BaseModel

from ..models.Mentor import TechnologyProficiency
from ..schemas.Attendee import ShirtSize, ProgrammingExperience


class Mentor(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone_number: str
    occupation: str
    country: str
    address_line_one: str
    address_line_two: str
    city: str
    state_or_province: str = None
    postal_code: str
    birthdate: datetime.date
    gender: str
    ethnicity: str
    tshirt_size: ShirtSize
    twitter_handle: str = None
    github_username: str = None
    linkedin_profile: str = None
    programming_experience: ProgrammingExperience
    technology_proficiency: TechnologyProficiency
    proficient_in_languages: str = None
    specific_skills: str = None

    class Config:
        orm_mode = True
