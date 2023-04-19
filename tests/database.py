
from db import Base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine
from config import (
    TEST_DB_NAME,
    TEST_DB_PASSWORD,
    TEST_DB_PORT,
    TEST_DB_SEVER_ADDRESS,
    TEST_DB_USERNAME
)

test_engine = create_engine("postgresql://{}:{}@{}:{}/{}".format(
    TEST_DB_USERNAME,
    TEST_DB_PASSWORD,
    TEST_DB_SEVER_ADDRESS,
    TEST_DB_PORT,
    TEST_DB_NAME
))

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
Base.metadata.create_all(bind=test_engine)


def get_test_db() -> Session:
    try:
        test_db = TestSessionLocal()
        yield test_db

    finally:
        test_db.close()
