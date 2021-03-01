from pydantic import BaseModel

from .Attendee import ShirtSize


class Mentor(BaseModel):
    first_name : str
    last_name : str
    email : str
    phone_number : str
    occupation : str
    college_student : str = None
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
    programming_experience : int = None
    technology_proficiency : int = None
    proficent_in_languages : str = None
    specific_skills : str = None
