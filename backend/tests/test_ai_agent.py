"""
Tests for AI Agent
"""

import pytest

from models.schemas import LeadInput, LeadPriority, LeadSource
from services.ai_agent import LeadQualificationAgent


@pytest.fixture
def agent():
    """Create AI agent instance"""
    return LeadQualificationAgent()


@pytest.mark.asyncio
async def test_agent_initialization(agent):
    """Test agent initializes correctly"""
    assert agent is not None
    assert agent.model is not None


@pytest.mark.asyncio
async def test_qualify_high_intent_lead(agent):
    """Test qualification of high-intent lead"""
    lead = LeadInput(
        name="Sarah Johnson",
        email="sarah@bigcorp.com",
        company="BigCorp Inc",
        phone="+1234567890",
        message=(
            "We urgently need a CRM solution for our 200-person sales team. "
            "We have budget approved for $100k and need to implement ASAP. "
            "Our current system is failing and costing us deals."
        ),
        source=LeadSource.REFERRAL,
    )

    result = await agent.qualify_lead(lead)

    assert result["score"] > 60
    assert result["priority"] in [LeadPriority.HOT, LeadPriority.WARM]
    assert result["analysis"] is not None
    assert len(result["analysis"].pain_points) > 0


@pytest.mark.asyncio
async def test_qualify_low_intent_lead(agent):
    """Test qualification of low-intent lead"""
    lead = LeadInput(
        name="Bob Smith",
        email="bob@personal.com",
        message="Just curious about your product. No rush.",
        source=LeadSource.WEB_FORM,
    )

    result = await agent.qualify_lead(lead)

    assert result["score"] < 70
    assert result["analysis"] is not None


@pytest.mark.asyncio
async def test_score_calculation(agent):
    """Test score calculation logic"""
    # High urgency, ready to buy
    analysis_data = {
        "urgency_level": "high",
        "buying_intent": "ready_to_buy",
        "budget_signals": ["approved budget", "timeline", "decision maker"],
        "pain_points": [
            "current system failing",
            "losing deals",
            "team frustrated",
            "competitors ahead",
        ],
    }

    score = agent._calculate_score(analysis_data)

    # High urgency (30) + ready to buy (40) + 3 budget signals (15)
    # + 4 pain points (15) = 100
    assert score == 100.0


@pytest.mark.asyncio
async def test_score_calculation_low(agent):
    """Test low score calculation"""
    analysis_data = {
        "urgency_level": "low",
        "buying_intent": "just_browsing",
        "budget_signals": [],
        "pain_points": ["curious"],
    }

    score = agent._calculate_score(analysis_data)

    # Low urgency (10) + browsing (10) + no budget (0) + 1 pain point (4) = 24
    assert score == 24.0


@pytest.mark.asyncio
async def test_priority_determination(agent):
    """Test priority assignment based on score"""
    assert agent._determine_priority(85) == LeadPriority.HOT
    assert agent._determine_priority(70) == LeadPriority.WARM
    assert agent._determine_priority(50) == LeadPriority.COLD
