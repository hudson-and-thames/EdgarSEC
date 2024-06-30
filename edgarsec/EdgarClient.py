import json
from typing import Dict, Any, Optional
import requests
from ratelimit import limits, sleep_and_retry
from edgarsec.models import CIK, Period
import logging
from edgarsec.errors import RequestFailedException, InvalidCIKException
from edgarsec.utils import _download_file, _unzip_file
from pathlib import Path


class EdgarClient:
    BASE_URL = "https://data.sec.gov"
    ARCHIVES_URL = "https://www.sec.gov/Archives/edgar/daily-index"
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
    def _make_request(self, url: str, params: Optional[Dict[str, Any]] = None,
                      stream: Optional[bool] = None) -> requests.Response:
        try:
            response = self.session.get(url, params=params, stream=stream)
            response.raise_for_status()
            return response
        except requests.exceptions.HTTPError as err:
            self.logger.error(f"Request failed with error: {err}")
            raise RequestFailedException(f"Request failed with error: {err}")

    def _parse_response_json(self, content: bytes) -> Dict[str, Any]:
        try:
            return json.loads(content)
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse JSON response: {e}")
            raise ValueError(f"Failed to parse JSON response: {e}")

    def get_company_filings(self, cik: str) -> Dict[str, Any]:
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

    def get_frames(self, period: str) -> Dict[str, Any]:
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

    def __download_file__(self, url: str, file_path: str | Path, unzip: bool = False) -> None:
        file_path = Path(file_path)
        self.logger.info(f"Downloading file from: {url}")
        response = self._make_request(url=url, stream=True)
        self.logger.info(f"Download and Save  file to: {file_path.absolute()}")
        _download_file(response, file_path=file_path)

        if unzip:
            self.logger.info(f"Unzipping file to: {file_path.parent}")
            _unzip_file(file_path=file_path, extract_to=file_path.parent)

    def download_company_facts(self, file_path: str | Path, unzip: bool = False) -> None:
        url = f"{self.ARCHIVES_URL}/xbrl/companyfacts.zip"
        self.__download_file__(url=url, file_path=file_path, unzip=unzip)

    def download_filing_history(self, file_path: str | Path, unzip: bool = False) -> None:
        url = f"{self.ARCHIVES_URL}/bulkdata/submissions.zip"
        self.__download_file__(url=url, file_path=file_path, unzip=unzip)
