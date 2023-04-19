import os
import pytest
from unittest import mock
from app import app
from db import Base
from db import get_db
from tests.database import get_test_db, test_engine
from fastapi.testclient import TestClient


@pytest.fixture(scope='session')
def client():
    app.dependency_overrides[get_db] = get_test_db
    Base.metadata.create_all(bind=test_engine)
    with mock.patch.dict(os.environ, {"TESTING": "Testing"}):
        yield TestClient(app)
    Base.metadata.drop_all(bind=test_engine)
