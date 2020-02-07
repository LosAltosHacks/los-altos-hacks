from typing import List

from pydantic import BaseModel

from .Attendee import ShirtSize


class Mentor(BaseModel):
    class Timeslot(BaseModel):
        start_time: str
        end_time: str

    first_name: str
    last_name: str
    over_18: bool
    company: str
    email: str
    phone_number: str
    tshirt_size: ShirtSize
    timeslots: List[Timeslot]
    skillset: str = None
    dietary_restrictions: str = None
