import json
from typing import Dict, Any, Optional
import requests
from ratelimit import limits, sleep_and_retry
from edgarsec.models import CIK, Period
import logging
from edgarsec.errors import RequestFailedException, InvalidCIKException


class EdgarClient:
    BASE_URL = "https://data.sec.gov"
    USER_AGENT = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) "
                  "Version/17.5 Safari/605.1.15")  # TODO: should be change
    MAX_CALLS_PER_SECOND = 10

    def __init__(self, user_agent: Optional[str] = None, logger: Optional[logging.Logger] = None):
        self.session = requests.Session()
        self.USER_AGENT = user_agent or self.USER_AGENT
        self.session.headers.update({'User-Agent': self.USER_AGENT})
        self.logger = logger or logging.getLogger(__name__)

    def __exit__(self, exc_type, exc_value, traceback):
        self.session.close()

    @sleep_and_retry
    @limits(calls=MAX_CALLS_PER_SECOND, period=1)
    def _make_request(self, url: str, params: Optional[Dict[str, Any]] = None) -> requests.Response:
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as err:
            self.logger.error(f"Request failed with error: {err}")
            raise RequestFailedException(f"Request failed with error: {err}")

    def _parse_response_json(self, content: bytes) -> Dict[str, Any]:
        """
        Parse the JSON response from the SEC EDGAR API.

        :param content: Binary content of the response.
        :return: JSON containing filing information.
        """
        try:
            return json.loads(content)
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse JSON response: {e}")
            raise ValueError(f"Failed to parse JSON response: {e}")

    def get_company_filings(self, cik: str) -> Dict[str, Any]:
        """
        Get filings for a specific company.

        :param cik: Central Index Key (CIK) of the company.
        :return: Dictionary containing filing information.
        :raises InvalidCIKException: If the CIK is invalid.
        :raises RequestFailedException: If the request fails.
        """
        cik_obj = CIK(cik)
        try:
            cik_obj.verify_cik()
        except ValueError as e:
            self.logger.error(f"Invalid CIK: {e}")
            raise InvalidCIKException(f"Invalid CIK: {e}")

        url = f"{self.BASE_URL}/submissions/CIK{cik_obj}.json"
        self.logger.info(f"Making request to: {url}")
        response = self._make_request(url)

        if response.status_code == 200:
            return self._parse_response_json(response.content)
        else:
            self.logger.error(f"Failed request with code: {response.status_code}")
            raise RequestFailedException(f"Failed request with code: {response.status_code}")

    def get_company_concept(self, cik: str) -> Dict[str, Any]:
        """
        Get concept for a specific company.

        :param cik: Central Index Key (CIK) of the company.
        :return: Dictionary containing concept information.
        :raises InvalidCIKException: If the CIK is invalid.
        :raises RequestFailedException: If the request fails.
        """
        cik_obj = CIK(cik)
        try:
            cik_obj.verify_cik()
        except ValueError as e:
            self.logger.error(f"Invalid CIK: {e}")
            raise InvalidCIKException(f"Invalid CIK: {e}")

        url = f"{self.BASE_URL}/api/xbrl/companyconcept/CIK{cik_obj}/us-gaap/AccountsPayableCurrent.json"
        self.logger.info(f"Making request to: {url}")
        response = self._make_request(url)

        if response.status_code == 200:
            return self._parse_response_json(response.content)
        else:
            self.logger.error(f"Failed request with code: {response.status_code}")
            raise RequestFailedException(f"Failed request with code: {response.status_code}")

    def get_company_facts(self, cik: str) -> Dict[str, Any]:
        """
        Get facts for a specific company.

        :param cik: Central Index Key (CIK) of the company.
        :return: Dictionary containing facts information.
        :raises InvalidCIKException: If the CIK is invalid.
        :raises RequestFailedException: If the request fails.
        """
        cik_obj = CIK(cik)
        try:
            cik_obj.verify_cik()
        except ValueError as e:
            self.logger.error(f"Invalid CIK: {e}")
            raise InvalidCIKException(f"Invalid CIK: {e}")

        url = f"{self.BASE_URL}/api/xbrl/companyfacts/CIK{cik_obj}.json"
        self.logger.info(f"Making request to: {url}")
        response = self._make_request(url)

        if response.status_code == 200:
            return self._parse_response_json(response.content)
        else:
            self.logger.error(f"Failed request with code: {response.status_code}")
            raise RequestFailedException(f"Failed request with code: {response.status_code}")

    def get_frames(self, period:str)-> Dict[str, Any]:
        """
        Get frames for a specific period.

        :param period: Period of the frame.
        :return: Dictionary containing frame information.
        :raises ValueError: If the period is invalid.
        :raises RequestFailedException: If the request fails.
        """
        period_obj = Period(period)
        try:
            period_obj.is_valid()
        except ValueError as e:
            self.logger.error(f"Invalid period: {e}")
            raise ValueError(f"Invalid period: {e}")

        url = f"{self.BASE_URL}/api/xbrl/frames/us-gaap/AccountsPayableCurrent/USD/{period_obj}.json"
        self.logger.info(f"Making request to: {url}")
        response = self._make_request(url)

        if response.status_code == 200:
            return self._parse_response_json(response.content)
        else:
            self.logger.error(f"Failed request with code: {response.status_code}")
            raise RequestFailedException(f"Failed request with code: {response.status_code}")

