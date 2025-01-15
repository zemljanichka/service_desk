import pytest
import pytest_asyncio
from app import app
from database import OperatorModel
from fastapi.testclient import TestClient
from utils import hash_password


@pytest.fixture
def client():
    with TestClient(app, base_url="http://test_api") as api:
        yield api


@pytest_asyncio.fixture()
async def test_operator():
    await OperatorModel.insert(username="test", hashed_password=hash_password("test"))
    yield
    await OperatorModel.delete(OperatorModel.username == "test")
