"""
Airtable client for lead management
"""

import json
import logging
from datetime import datetime
from typing import Dict, Optional

from pyairtable import Api

from config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class AirtableClient:
    """Client for interacting with Airtable"""

    def __init__(self):
        """Initialize Airtable client"""
        self.api = Api(settings.AIRTABLE_API_KEY)
        self.table = self.api.table(
            settings.AIRTABLE_BASE_ID, settings.AIRTABLE_TABLE_NAME
        )
        logger.info("✅ Airtable client initialized")

    def create_lead(self, lead_data: Dict) -> Optional[str]:
        """
        Create a new lead in Airtable

        Args:
            lead_data: Lead information including analysis

        Returns:
            Record ID if successful, None otherwise
        """
        try:
            # Prepare fields for Airtable
            fields = {
                "Name": lead_data["name"],
                "Email": lead_data["email"],
                "Phone": lead_data.get("phone", ""),
                "Company": lead_data.get("company", ""),
                "Website": lead_data.get("website", ""),
                "Message": lead_data["message"],
                "Source": lead_data["source"],
                "Score": float(lead_data["score"]),
                "Priority": lead_data["priority"],
                "Status": "new",
                # Don't send Created At - Airtable auto-creates it
            }

            # Add AI analysis fields
            analysis = lead_data.get("analysis", {})
            if analysis:
                fields["Industry"] = analysis.get("industry", "")
                fields["Company Size"] = analysis.get("company_size", "")
                fields["Urgency Level"] = analysis.get("urgency_level", "medium")
                fields["Buying Intent"] = analysis.get("buying_intent", "")
                fields["Recommended Action"] = analysis.get("recommended_action", "")

                # Store arrays as JSON strings
                if analysis.get("pain_points"):
                    fields["Pain Points"] = json.dumps(analysis["pain_points"])
                if analysis.get("budget_signals"):
                    fields["Budget Signals"] = json.dumps(analysis["budget_signals"])

            # Create record
            record = self.table.create(fields)

            logger.info(
                "✅ Lead created in Airtable: %s (ID: %s)",
                lead_data["name"],
                record["id"],
            )

            return record["id"]

        except Exception as e:
            logger.error("❌ Failed to create lead in Airtable: %s", str(e))
            return None

    def update_lead(self, record_id: str, updates: Dict) -> bool:
        """
        Update an existing lead

        Args:
            record_id: Airtable record ID
            updates: Fields to update

        Returns:
            True if successful, False otherwise
        """
        try:
            self.table.update(record_id, updates)
            logger.info("✅ Lead updated in Airtable: %s", record_id)
            return True

        except Exception as e:
            logger.error("❌ Failed to update lead in Airtable: %s", str(e))
            return False

    def get_lead(self, record_id: str) -> Optional[Dict]:
        """
        Get a lead by record ID

        Args:
            record_id: Airtable record ID

        Returns:
            Lead data if found, None otherwise
        """
        try:
            record = self.table.get(record_id)
            return record["fields"]

        except Exception as e:
            logger.error("❌ Failed to get lead from Airtable: %s", str(e))
            return None

    def list_leads(self, priority: Optional[str] = None, limit: int = 100) -> list:
        """
        List leads with optional filtering

        Args:
            priority: Filter by priority (hot, warm, cold)
            limit: Maximum number of records to return

        Returns:
            List of lead records
        """
        try:
            formula = None
            if priority:
                formula = f"{{Priority}} = '{priority}'"

            records = self.table.all(
                formula=formula, max_records=limit, sort=["-Created At"]
            )

            logger.info("✅ Retrieved %s leads from Airtable", len(records))
            return records

        except Exception as e:
            logger.error("❌ Failed to list leads from Airtable: %s", str(e))
            return []

    def get_stats(self) -> Dict:
        """
        Get lead statistics

        Returns:
            Dictionary with stats
        """
        try:
            all_leads = self.table.all()

            stats = {
                "total": len(all_leads),
                "hot": 0,
                "warm": 0,
                "cold": 0,
                "avg_score": 0.0,
            }

            if all_leads:
                scores = []
                for record in all_leads:
                    fields = record["fields"]
                    priority = fields.get("Priority", "").lower()

                    if priority == "hot":
                        stats["hot"] += 1
                    elif priority == "warm":
                        stats["warm"] += 1
                    elif priority == "cold":
                        stats["cold"] += 1

                    score = fields.get("Score")
                    if score:
                        scores.append(score)

                if scores:
                    stats["avg_score"] = sum(scores) / len(scores)

            logger.info("✅ Retrieved stats from Airtable")
            return stats

        except Exception as e:
            logger.error("❌ Failed to get stats from Airtable: %s", str(e))
            return {
                "total": 0,
                "hot": 0,
                "warm": 0,
                "cold": 0,
                "avg_score": 0,
            }
