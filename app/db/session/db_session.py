from dotenv import load_dotenv
from os import environ
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from core.config import dev_settings, prod_settings

load_dotenv()


debug = bool(environ.get("DEBUG"))
engine = create_engine(
    prod_settings.DATABASE_URI if not debug else dev_settings.DATABASE_URI
)

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)
