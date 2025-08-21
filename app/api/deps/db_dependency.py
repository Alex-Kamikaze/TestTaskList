from db.session.db_session import SessionLocal
from sqlalchemy.orm import Session
from typing import Generator

def get_db() -> Generator[Session, any, any]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()