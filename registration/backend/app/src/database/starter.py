from sqlalchemy import MetaData
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from main import app

# Made using the database tutorial here
# https://fastapi.tiangolo.com/tutorial/sql-databases/

engine = create_engine(
    app.config('SQLALCHEMY_DATABASE_URL')
)

metadata = MetaData()
metadata.reflect(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

dbBase = declarative_base()
