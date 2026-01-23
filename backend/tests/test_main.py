"""
Tests for FastAPI endpoints
"""


def test_root_endpoint(client):
    """Test root endpoint returns health check"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "services" in data
    assert "timestamp" in data


def test_health_check(client):
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "api" in data["services"]


def test_test_endpoint(client):
    """Test simple test endpoint"""
    response = client.get("/test")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_qualify_lead_success(client, sample_lead):
    """Test lead qualification with valid data"""
    response = client.post("/leads", json=sample_lead)
    assert response.status_code == 200

    data = response.json()
    assert data["success"] is True
    assert "qualified_lead" in data
    assert "processing_time" in data

    # Check qualified lead structure
    lead = data["qualified_lead"]
    assert lead["name"] == sample_lead["name"]
    assert lead["email"] == sample_lead["email"]
    assert "score" in lead
    assert "priority" in lead
    assert "analysis" in lead

    # Score should be between 0 and 100
    assert 0 <= lead["score"] <= 100


def test_qualify_lead_low_score(client, low_quality_lead):
    """Test that low quality leads get lower scores"""
    response = client.post("/leads", json=low_quality_lead)
    assert response.status_code == 200

    data = response.json()
    lead = data["qualified_lead"]

    # Low quality lead should have lower score
    assert lead["score"] < 60
    assert lead["priority"] in ["cold", "warm"]


def test_qualify_lead_invalid_email(client):
    """Test validation fails for invalid email"""
    invalid_lead = {
        "name": "Test User",
        "email": "not-an-email",
        "message": "This is a test message",
        "source": "web_form",
    }
    response = client.post("/leads", json=invalid_lead)
    assert response.status_code == 422  # Validation error


def test_qualify_lead_missing_required_fields(client):
    """Test validation fails for missing required fields"""
    incomplete_lead = {
        "name": "Test User",
        # Missing email and message
    }
    response = client.post("/leads", json=incomplete_lead)
    assert response.status_code == 422


def test_qualify_lead_message_too_short(client):
    """Test validation fails for too short message"""
    short_message_lead = {
        "name": "Test User",
        "email": "test@example.com",
        "message": "Short",  # Less than 10 characters
        "source": "web_form",
    }
    response = client.post("/leads", json=short_message_lead)
    assert response.status_code == 422
