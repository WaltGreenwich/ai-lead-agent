"""
Data models and schemas
"""

from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field, HttpUrl


class LeadSource(str, Enum):
    """Lead source types"""

    WEB_FORM = "web_form"
    EMAIL = "email"
    PHONE = "phone"
    REFERRAL = "referral"
    OTHER = "other"


class LeadPriority(str, Enum):
    """Lead priority levels"""

    HOT = "hot"  # Score > 80
    WARM = "warm"  # Score 60-79
    COLD = "cold"  # Score < 60


class LeadInput(BaseModel):
    """Input schema for new lead"""

    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    phone: Optional[str] = None
    company: Optional[str] = None
    website: Optional[HttpUrl] = None
    message: str = Field(..., min_length=10, max_length=1000)
    source: LeadSource = LeadSource.WEB_FORM


class AIAnalysis(BaseModel):
    """AI analysis result"""

    industry: Optional[str] = None
    company_size: Optional[str] = None
    budget_signals: List[str] = Field(default_factory=list)
    pain_points: List[str] = Field(default_factory=list)
    urgency_level: str = "medium"
    buying_intent: str = "exploring"
    recommended_action: str


class QualifiedLead(BaseModel):
    """Fully qualified lead with AI analysis"""

    # Original data
    name: str
    email: str
    phone: Optional[str] = None
    company: Optional[str] = None
    website: Optional[str] = None
    message: str
    source: LeadSource

    # AI Analysis
    score: float = Field(..., ge=0, le=100)
    priority: LeadPriority
    analysis: AIAnalysis

    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    assigned_to: Optional[str] = None
    status: str = "new"


class LeadResponse(BaseModel):
    """API response for lead submission"""

    success: bool
    lead_id: Optional[str] = None
    qualified_lead: Optional[QualifiedLead] = None
    error: Optional[str] = None
    processing_time: float


class HealthCheck(BaseModel):
    """Health check response"""

    status: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    services: dict
