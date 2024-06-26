import json
from typing import Dict, Any
import requests
from ratelimit import limits, sleep_and_retry
from edgarsec.types import CIK


class EdgarClient:
    BASE_URL = "https://data.sec.gov"
    USER_AGENT = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) "
                  "Version/17.5 Safari/605.1.15")   # TODO: should be change
    MAX_CALLS_PER_SECOND = 10

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': self.USER_AGENT})

    @sleep_and_retry
    @limits(calls=MAX_CALLS_PER_SECOND, period=1)
    def _make_request(self, url, params=None):
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response

    def get_company_filings(self, cik: str):
        """
        Get filings for a specific company.

        :param cik: Central Index Key (CIK) of the company.
        :return: DataFrame containing filing information.
        """
        cik = CIK(cik)
        cik.verify_cik()
        url = f"{self.BASE_URL}/submissions/CIK{cik}.json"
        response = self._make_request(url)

        if response.status_code == 200:
            return self._parse_response_json(response.content)

    @staticmethod
    def _parse_response_json(content) -> Dict[str, Any] | None:
        """
        Parse the JSON response from the SEC EDGAR API.

        :param content: Binary content of the response.
        :return: JSON containing filing information.
        """
        try:
            return json.loads(content)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON response: {e}")