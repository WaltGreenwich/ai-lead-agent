"""
FastAPI main application
"""

import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from config import get_settings
from models.schemas import HealthCheck, LeadInput, LeadResponse
from services.ai_agent import LeadQualificationAgent

settings = get_settings()


# Lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Startup
    print("🚀 Starting AI Lead Agent...")
    yield
    # Shutdown
    print("👋 Shutting down AI Lead Agent...")


# Initialize FastAPI app
app = FastAPI(
    title="AI Lead Qualification Agent",
    description="Intelligent lead scoring and qualification using Google Gemini",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize AI Agent
agent = LeadQualificationAgent()


@app.get("/", response_model=HealthCheck)
async def root():
    """Root endpoint - health check"""
    return HealthCheck(
        status="healthy",
        services={
            "ai_agent": "operational",
            "gemini_api": "connected",
        },
    )


@app.get("/health", response_model=HealthCheck)
async def health_check():
    """Detailed health check"""
    return HealthCheck(
        status="healthy",
        services={
            "api": "running",
            "ai_agent": "operational",
            "gemini_api": "connected",
        },
    )


@app.post("/leads", response_model=LeadResponse)
async def qualify_lead(lead: LeadInput):
    """
    Qualify a new lead using AI analysis

    Args:
        lead: Lead information

    Returns:
        LeadResponse with qualification results
    """
    start_time = time.time()

    try:
        # Qualify lead with AI
        result = await agent.qualify_lead(lead)

        # Build qualified lead object
        from models.schemas import QualifiedLead

        qualified_lead = QualifiedLead(
            name=lead.name,
            email=lead.email,
            phone=lead.phone,
            company=lead.company,
            website=str(lead.website) if lead.website else None,
            message=lead.message,
            source=lead.source,
            score=result["score"],
            priority=result["priority"],
            analysis=result["analysis"],
        )

        processing_time = time.time() - start_time

        return LeadResponse(
            success=True,
            lead_id=None,  # Will be set when Airtable is integrated
            qualified_lead=qualified_lead,
            processing_time=processing_time,
        )

    except Exception as e:
        processing_time = time.time() - start_time
        raise HTTPException(
            status_code=500,
            detail=f"Lead qualification failed: {str(e)}",
        ) from e


@app.get("/test")
async def test_endpoint():
    """Simple test endpoint"""
    return {"message": "Test endpoint working", "status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG,
    )
