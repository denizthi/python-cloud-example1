# app/database.py

# resource: https://neon.com/docs/guides/sqlalchemy-migrations#setting-up-your-database

import os

import dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

dotenv.load_dotenv()
SQLALCHEMY_DATABASE_URL_C = os.getenv("DATABASE_URL_C")

engine = create_engine(SQLALCHEMY_DATABASE_URL_C)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()