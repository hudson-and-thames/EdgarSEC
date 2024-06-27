import re


class Period:
    def __init__(self, period: str):
        self.period = period

    def is_valid(self):
        """
        Validate the period format.

        :raises ValueError: If the period is invalid.
        """
        # Regular expressions for valid period formats
        annual_pattern = r'^CY\d{4}$'  # e.g., CY2023
        quarterly_pattern = r'^CY\d{4}Q[1-4]$'  # e.g., CY2023Q1
        instantaneous_pattern = r'^CY\d{4}Q[1-4]I$'  # e.g., CY2023Q1I

        if not (re.match(annual_pattern, self.period) or
                re.match(quarterly_pattern, self.period) or
                re.match(instantaneous_pattern, self.period)):
            raise ValueError("Invalid period format.")

    def __str__(self):
        return self.period
