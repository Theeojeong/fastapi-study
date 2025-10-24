import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture
def client():
    return TestClient(app=app)

# tests 폴더 안에서 글로벌하게 client를 사용하는 방법
