from sqlmodel import Session, create_engine, SQLModel
from . config import settings

DATABASE_URL = settings.database_url


engine = create_engine(DATABASE_URL)

def get_engine():
    return engine

def create_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
