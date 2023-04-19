from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base

from config import DB_SEVER_ADDRESS, DB_USERNAME, DB_PASSWORD, DB_PORT, DB_NAME

engine = create_engine(
    "postgresql://{}:{}@{}:{}/{}".format(
        DB_USERNAME,
        DB_PASSWORD,
        DB_SEVER_ADDRESS,
        DB_PORT,
        DB_NAME
    ), pool_pre_ping=True, pool_recycle=3600
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
