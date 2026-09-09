
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import settings

USER = settings.db_user
PASSWORD = settings.db_pass
HOST = settings.db_host
PORT = settings.db_port
DB = settings.db_name

DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}?sslmode=require"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
mongo_client = None


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
