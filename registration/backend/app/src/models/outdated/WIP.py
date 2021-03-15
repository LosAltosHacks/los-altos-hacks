from sqlalchemy import Column, String, SmallInteger, Integer
from models.database import dbBase

class SignIn(dbBase):
    __tablename__ = "signin"

    id = Column(Integer, nullable=False, primary_key=True)
    badge_data = Column(String(128), nullable=False, unique=True)
    meal_1 = Column(SmallInteger, nullable=False, default=0)
    meal_2 = Column(SmallInteger, nullable=False, default=0)
    meal_3 = Column(SmallInteger, nullable=False, default=0)
    meal_4 = Column(SmallInteger, nullable=False, default=0)
    meal_5 = Column(SmallInteger, nullable=False, default=0)
    meal_7 = Column(SmallInteger, nullable=False, default=0)
    meal_8 = Column(SmallInteger, nullable=False, default=0)
    meal_9 = Column(SmallInteger, nullable=False, default=0)
