"""
Pytest configuration and fixtures
"""

import pytest
from fastapi.testclient import TestClient

from example_main import app
from models.schemas import LeadSource


@pytest.fixture(scope="session")
def anyio_backend():
    """Configure async backend for tests"""
    return "asyncio"


@pytest.fixture(scope="module")
def client():
    """Create test client"""
    return TestClient(app)


@pytest.fixture
def sample_lead():
    """Sample lead data for testing"""
    return {
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "+1234567890",
        "company": "Tech Corp",
        "website": "https://techcorp.com",
        "message": "We need a CRM solution urgently for our 50-person team. "
        "Budget is around $50k. Looking to implement within 2 weeks.",
        "source": LeadSource.WEB_FORM.value,
    }


@pytest.fixture
def low_quality_lead():
    """Low quality lead for testing"""
    return {
        "name": "Jane Smith",
        "email": "jane@personal.com",
        "message": "Just browsing, maybe interested",
        "source": LeadSource.WEB_FORM.value,
    }
