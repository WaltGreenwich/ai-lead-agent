"""
Tests for Airtable integration
"""

# pylint: disable=redefined-outer-name

import pytest

from services.airtable_client import AirtableClient


@pytest.fixture
def airtable_client():
    """Create Airtable client"""
    return AirtableClient()


@pytest.fixture
def sample_lead_data():
    """Sample lead data for testing"""
    return {
        "name": "Test Lead",
        "email": "test@example.com",
        "phone": "+1234567890",
        "company": "Test Corp",
        "website": "https://test.com",
        "message": "Test message for Airtable integration",
        "source": "web_form",
        "score": 75,
        "priority": "warm",
        "analysis": {
            "industry": "Technology",
            "company_size": "Medium",
            "urgency_level": "medium",
            "buying_intent": "evaluating",
            "pain_points": ["test pain 1", "test pain 2"],
            "budget_signals": ["test signal"],
            "recommended_action": "Follow up in 2 days",
        },
    }


def test_airtable_client_initialization(airtable_client):
    """Test Airtable client initializes correctly"""
    assert airtable_client is not None
    assert airtable_client.table is not None


@pytest.mark.skip(reason="Requires actual Airtable credentials")
def test_create_lead(airtable_client, sample_lead_data):
    """Test creating a lead in Airtable"""
    record_id = airtable_client.create_lead(sample_lead_data)
    assert record_id is not None
    assert isinstance(record_id, str)


@pytest.mark.skip(reason="Requires actual Airtable credentials")
def test_get_lead(airtable_client, sample_lead_data):
    """Test retrieving a lead from Airtable"""
    # Create a lead first
    record_id = airtable_client.create_lead(sample_lead_data)
    assert record_id is not None

    # Retrieve it
    lead = airtable_client.get_lead(record_id)
    assert lead is not None
    assert lead["Name"] == sample_lead_data["name"]
    assert lead["Email"] == sample_lead_data["email"]


@pytest.mark.skip(reason="Requires actual Airtable credentials")
def test_update_lead(airtable_client, sample_lead_data):
    """Test updating a lead in Airtable"""
    # Create a lead first
    record_id = airtable_client.create_lead(sample_lead_data)
    assert record_id is not None

    # Update it
    success = airtable_client.update_lead(record_id, {"Status": "contacted"})
    assert success is True

    # Verify update
    lead = airtable_client.get_lead(record_id)
    assert lead["Status"] == "contacted"


@pytest.mark.skip(reason="Requires actual Airtable credentials")
def test_list_leads(airtable_client):
    """Test listing leads from Airtable"""
    leads = airtable_client.list_leads(limit=10)
    assert isinstance(leads, list)


@pytest.mark.skip(reason="Requires actual Airtable credentials")
def test_get_stats(airtable_client):
    """Test getting statistics from Airtable"""
    stats = airtable_client.get_stats()
    assert isinstance(stats, dict)
    assert "total" in stats
    assert "hot" in stats
    assert "warm" in stats
    assert "cold" in stats
    assert "avg_score" in stats
