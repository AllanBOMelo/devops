import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", f"mysql+pymysql://{user}:{password}@db/test_db")

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"host": "db", "port": 3306})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
