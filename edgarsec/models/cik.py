class CIK:
    def __init__(self, cik: str):
        self.cik = cik

    def verify_cik(self):
        """
        Verify if the CIK is valid.

        :raises ValueError: If the CIK is invalid.

        """
        if not self.cik.isdigit() or len(self.cik) != 10:
            raise ValueError("CIK should be a 10-digit number.")

    def __str__(self):
        return self.cik
