"""
AI Agent for lead qualification using Google Gemini
"""

import json
import logging
from typing import Dict

import google.generativeai as genai

from config import get_settings
from models.schemas import AIAnalysis, LeadInput, LeadPriority

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

settings = get_settings()


class LeadQualificationAgent:
    """
    AI Agent that qualifies leads using Gemini

    Responsibilities:
    - Analyze lead message for intent and urgency
    - Extract pain points and budget signals
    - Determine industry and company size
    - Generate lead score (0-100)
    - Recommend next action
    """

    def __init__(self):
        """Initialize Gemini AI"""
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel("gemini-pro")
        logger.info("✅ AI Agent initialized with Gemini")

    async def qualify_lead(self, lead: LeadInput) -> Dict:
        """
        Qualify lead using AI analysis

        Args:
            lead: Input lead data

        Returns:
            Dict with score, priority, and analysis
        """
        try:
            logger.info(f"🤖 Analyzing lead: {lead.name}")

            # Build analysis prompt
            prompt = self._build_prompt(lead)

            # Call Gemini
            response = self.model.generate_content(prompt)

            # Parse response
            analysis_data = self._parse_response(response.text)

            # Calculate score and priority
            score = self._calculate_score(analysis_data)
            priority = self._determine_priority(score)

            # Build AI Analysis object
            analysis = AIAnalysis(
                industry=analysis_data.get("industry"),
                company_size=analysis_data.get("company_size"),
                budget_signals=analysis_data.get("budget_signals", []),
                pain_points=analysis_data.get("pain_points", []),
                urgency_level=analysis_data.get("urgency_level", "medium"),
                buying_intent=analysis_data.get("buying_intent", "exploring"),
                recommended_action=analysis_data.get(
                    "recommended_action", "Follow up within 24 hours"
                ),
            )

            logger.info(
                f"✅ Lead qualified: {lead.name} (Score: {score}, Priority: {priority})"
            )

            return {"score": score, "priority": priority, "analysis": analysis}

        except Exception as e:
            logger.error(f"❌ AI analysis failed: {str(e)}")
            # Return default safe values
            return {
                "score": 50.0,
                "priority": LeadPriority.WARM,
                "analysis": AIAnalysis(
                    recommended_action="Manual review required - AI analysis failed"
                ),
            }

    def _build_prompt(self, lead: LeadInput) -> str:
        """Build analysis prompt for Gemini"""
        return f"""You are a lead qualification expert.
        Analyze this lead and provide structured insights.

Lead Information:
- Name: {lead.name}
- Email: {lead.email}
- Company: {lead.company or 'Not provided'}
- Website: {lead.website or 'Not provided'}
- Message: {lead.message}
- Source: {lead.source}

Analyze and provide a JSON response with:
{{
  "industry": "Primary industry of the company (or 'Unknown')",
  "company_size": "Estimated size: Startup/Small/Medium/Large/Enterprise",
  "budget_signals": ["List of 0-3 signals indicating budget/buying power"],
  "pain_points": ["List of 2-4 business pain points mentioned or implied"],
  "urgency_level": "high/medium/low based on language and context",
  "buying_intent": "ready_to_buy/evaluating/exploring/just_browsing",
  "recommended_action": "Specific next step for sales team (one sentence)"
}}

Important:
- Be realistic with company_size estimation
- Identify REAL pain points from the message
- urgency_level: "high" only if explicit urgency keywords present
- buying_intent: Consider actual purchase signals
- recommended_action: Be specific and actionable

Respond ONLY with valid JSON, no explanation or markdown.
"""

    def _parse_response(self, response_text: str) -> Dict:
        """Parse Gemini response to dict"""
        try:
            # Clean response
            cleaned = response_text.strip()

            # Remove markdown code blocks if present
            if cleaned.startswith("```json"):
                cleaned = cleaned[7:]
            if cleaned.startswith("```"):
                cleaned = cleaned[3:]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]

            cleaned = cleaned.strip()

            # Parse JSON
            return json.loads(cleaned)

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse AI response: {str(e)}")
            logger.error(f"Response was: {response_text}")

            # Return minimal safe structure
            return {
                "industry": "Unknown",
                "company_size": "Unknown",
                "budget_signals": [],
                "pain_points": ["Analysis failed - manual review needed"],
                "urgency_level": "medium",
                "buying_intent": "exploring",
                "recommended_action": "Manual review required",
            }

    def _calculate_score(self, analysis: Dict) -> float:
        """
        Calculate lead score based on AI analysis

        Scoring factors:
        - Urgency: 30 points (high=30, medium=20, low=10)
        - Buying intent: 40 points (ready=40, evaluating=30, exploring=20, browsing=10)
        - Budget signals: 15 points (3 signals=15, 2=10, 1=5, 0=0)
        - Pain points identified: 15 points (4+=15, 3=12, 2=8, 1=4)

        Total: 100 points
        """
        score = 0.0

        # Urgency (30 points)
        urgency_scores = {"high": 30, "medium": 20, "low": 10}
        score += urgency_scores.get(analysis.get("urgency_level", "medium"), 20)

        # Buying intent (40 points)
        intent_scores = {
            "ready_to_buy": 40,
            "evaluating": 30,
            "exploring": 20,
            "just_browsing": 10,
        }
        score += intent_scores.get(analysis.get("buying_intent", "exploring"), 20)

        # Budget signals (15 points)
        budget_signals = len(analysis.get("budget_signals", []))
        if budget_signals >= 3:
            score += 15
        elif budget_signals == 2:
            score += 10
        elif budget_signals == 1:
            score += 5

        # Pain points (15 points)
        pain_points = len(analysis.get("pain_points", []))
        if pain_points >= 4:
            score += 15
        elif pain_points == 3:
            score += 12
        elif pain_points == 2:
            score += 8
        elif pain_points == 1:
            score += 4

        return min(score, 100.0)  # Cap at 100

    def _determine_priority(self, score: float) -> LeadPriority:
        """Determine lead priority based on score"""
        if score >= settings.HIGH_SCORE_THRESHOLD:
            return LeadPriority.HOT
        elif score >= settings.MEDIUM_SCORE_THRESHOLD:
            return LeadPriority.WARM
        else:
            return LeadPriority.COLD
