from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL


SQLALCHEMY_DATABASE_URL = URL.create(
    drivername="postgresql",
    username="postgres",
    password="postgres",
    host="localhost",
    database="playonpaper",
)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
