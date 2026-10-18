# app/database.py

import os

import dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

dotenv.load_dotenv()
SQLALCHEMY_DATABASE_URL_X = os.getenv("DATABASE_URL_X")

engine = create_engine(SQLALCHEMY_DATABASE_URL_X)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()