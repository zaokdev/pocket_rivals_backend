import os
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from sqlalchemy import create_engine

from models.models import Base


load_dotenv()

engine = create_engine(
    os.getenv("DB_URL"),
    echo=True,
    pool_size=2,
    max_overflow=0,
    pool_recycle=3600,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(bind=engine)


def init_db(app):
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET")
    Base.metadata.create_all(bind=engine)
