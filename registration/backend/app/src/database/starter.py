from sqlalchemy import MetaData
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# This is causing circular import
# from main import app

# Made using the database tutorial here
# https://fastapi.tiangolo.com/tutorial/sql-databases/
SQLALCHEMY_DATABASE_URL = "" 

engine = create_engine(
    # app.config('SQLALCHEMY_DATABASE_URL')
    SQLALCHEMY_DATABASE_URL
)

metadata = MetaData()
metadata.reflect(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

dbBase = declarative_base()
