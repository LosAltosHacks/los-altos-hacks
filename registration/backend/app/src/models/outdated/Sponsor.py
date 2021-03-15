from outdated.Associate import DBAssociate
from models.Person import DBPerson
from outdated.Positioned import DBPositioned

from sqlalchemy.orm import relationship


class DBSponser(DBPerson, DBAssociate, DBPositioned):
    __tablename__ = "sponsors"

    timeslots = relationship("DBTimeslots", order_by="start_time.id", backref="sponsors")

    __mapper_args__ = {
        "polymorphic_identity": "sponsors"
    }