from sqlalchemy import Column, String, Boolean

from database.starter import dbBase


class DBHost(dbBase):
    __tablename__ = "hosts"

    email = Column(String(255), nullable=False, primary_key=True)
    password = Column(String(60), nullable=False)
    disabled = Column(Boolean(), nullable=False, default=False)
