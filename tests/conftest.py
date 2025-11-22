"""
Pytest configuration and fixtures.
"""

import pytest
from fastapi.testclient import TestClient
from mongomock import MongoClient

from backend.main import app
from backend.core.config import get_settings

@pytest.fixture
def test_app():
    """
    Create a test FastAPI application.
    """
    return TestClient(app)

@pytest.fixture
def mock_db():
    """
    Create a mock MongoDB client.
    """
    return MongoClient().db

@pytest.fixture
def test_settings():
    """
    Get test settings.
    """
    settings = get_settings()
    settings.MONGODB_URI = "mongomock://localhost"
    settings.TESTING = True
    return settings 