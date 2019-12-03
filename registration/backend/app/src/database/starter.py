from sqlalchemy import MetaData
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Made using the database tutorial here
# https://fastapi.tiangolo.com/tutorial/sql-databases/

# SQLALCHEMY_DATABASE_URL = "postgresql://localhost:5432/testregistration
SQLALCHEMY_DATABASE_URL = "SOON_TO_BE_OS_VENV™™"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

metadata = MetaData()
metadata.reflect(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

dbBase = declarative_base()
