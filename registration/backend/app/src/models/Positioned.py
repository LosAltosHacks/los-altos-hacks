from sqlalchemy import Column, String, Integer, ForeignKey

from .Person import DBPerson


class DBPositioned(DBPerson):
    __tablename__ = "judges"

    id = Column(Integer, nullable=False, primary_key=True)
    user_id = Column(String(36), ForeignKey('person.user_id'), nullable=False)
    position = Column(String(1000), nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "Positioned",
    }
