from pydantic import BaseModel

from .Attendee import ShirtSize


class Mentor(BaseModel):
    first_name: str
    last_name: str
    email: str
    tshirt_size: ShirtSize
    over_18: bool
    skillset: str = None
