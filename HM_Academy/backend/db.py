from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey


#engine = create_engine('sqlite:///db_academy.db', echo=True)
engine = create_engine('sqlite:///db_academy.db', echo=False)
#engine = create_engine('sqlite:///HM_Academy/db_academy.db', echo=True)
SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Base(DeclarativeBase):
    pass