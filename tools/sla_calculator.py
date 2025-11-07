from datetime import datetime, timedelta
form langfuse import observe

class SLACalculator:
    """Calculate SLA deadlines for support tickets"""
    SLA_HOURS = {
        "critical":4,
        "high":24,
        "medium":48,
        "low":72
    }

    @observe(as_type="tool")
    def calculate_deadline(self, urgency: str) -> str:
        """
        Calculate SLA deadline

        Args:
            urgency: "critical", "high", "medium", "low"

        Returns:
            ISO format datetime string
        """
        urgency = urgency.lower()
        if urgency not in self.SLA_HOURS:
            raise ValueError("Invalid urgency level")