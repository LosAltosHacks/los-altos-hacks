import config
from sqlalchemy import MetaData
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# This is causing circular import
# from main import app

# Made using the database tutorial here
# https://fastapi.tiangolo.com/tutorial/sql-databases/

engine = create_engine(
    config.SQLALCHEMY_DATABASE_URL
)

metadata = MetaData()
metadata.reflect(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

dbBase = declarative_base()

# Actually do the creating of tables, which is deferred until all necessary
# models have been imported by other code
def do_create_all():
    dbBase.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

