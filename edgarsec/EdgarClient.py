import json
from typing import Dict, Any, Optional, LiteralString, Literal
import requests
import certifi
import ssl
import aiofiles

from aiohttp import ClientResponse
from ratelimit import limits, sleep_and_retry
from tqdm import tqdm

from edgarsec.models import CIK, Period
import logging
from edgarsec.errors import RequestFailedException, InvalidCIKException
from edgarsec.utils import _download_file, _unzip_file
from pathlib import Path
import aiohttp
import asyncio


class EdgarClient:
    DATA_URL = "https://data.sec.gov"
    BASE_URL = "https://www.sec.gov"
    USER_AGENT = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) "
                  "Version/17.5 Safari/605.1.15")  # TODO: should be changed
    MAX_CALLS_PER_SECOND = 10

    def __init__(self, user_agent: Optional[str] = None, logger: Optional[logging.Logger] = None):
        self.session = aiohttp.ClientSession(
            headers={'User-Agent': self.USER_AGENT, 'Accept': 'application/json', 'Connection': 'keep-alive'}, )
        self.USER_AGENT = user_agent or self.USER_AGENT
        self.logger = logger or logging.getLogger(__name__)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()

    async def close(self):
        await self.session.close()

    @sleep_and_retry
    @limits(calls=MAX_CALLS_PER_SECOND, period=1)
    async def _make_request(self, url: str, params: Optional[Dict[str, Any]] = None,
                            stream: Optional[bool] = None) -> bytes:
        try:
            async with self.session.get(url, ssl=ssl.create_default_context(cafile=certifi.where())) as response:
                response.raise_for_status()
                return await response.read()
        except aiohttp.ClientError as err:
            self.logger.error(f"Request failed with error: {err}")
            raise RequestFailedException(f"Request failed with error: {err}")

    async def _download_file(self, url: str, file_path: str | Path, unzip: bool = False) -> None:

        file_path = Path(file_path)
        if not file_path.parent.exists():
            file_path.parent.mkdir(parents=True, exist_ok=True)
        self.logger.info(f"Downloading file from: {url}")
        chunk_size = 1024

        try:
            async with self.session.get(url, ssl=ssl.create_default_context(cafile=certifi.where())) as response:
                response.raise_for_status()
                total_size = int(response.headers.get('content-length', 0))
                with tqdm(total=total_size, unit='B', unit_scale=True, desc='Downloading File') as pbar:
                    async with aiofiles.open(file_path, mode='wb') as file:
                        async for chunk in response.content.iter_chunked(chunk_size):
                            await file.write(chunk)
                            pbar.update(len(chunk))

        except aiohttp.ClientError as err:
            self.logger.error(f"Request failed with error: {err}")
            raise RequestFailedException(f"Request failed with error: {err}")
        except  Exception as e:
            self.logger.error(f"Failed to download file: {e}")
            raise ValueError(f"Failed to download file: {e}")

        self.logger.info(f"Download and Save  file to: {file_path.absolute()}")

        if unzip:
            self.logger.info(f"Unzipping file to: {file_path.parent}")
            _unzip_file(file_path=file_path, extract_to=file_path.parent)

    def _parse_response_json(self, content: bytes) -> Dict[str, Any]:
        try:
            return json.loads(content)
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse JSON response: {e}")
            raise ValueError(f"Failed to parse JSON response: {e}")

    async def get_company_filings(self, cik: str) -> Dict[str, Any]:
        cik_obj = CIK(cik)
        try:
            cik_obj.verify_cik()
        except ValueError as e:
            self.logger.error(f"Invalid CIK: {e}")
            raise InvalidCIKException(f"Invalid CIK: {e}")

        url = f"{self.DATA_URL}/submissions/CIK{cik_obj}.json"
        self.logger.info(f"Making request to: {url}")
        response = await self._make_request(url)
        return self._parse_response_json(response)

    async def get_company_concept(self, cik: str, taxonomy: Literal["us-gaap",] = "us-gaap",
                                  tag: Literal["AccountsPayableCurrent"] = "AccountsPayableCurrent") -> Dict[str, Any]:
        cik_obj = CIK(cik)
        try:
            cik_obj.verify_cik()
        except ValueError as e:
            self.logger.error(f"Invalid CIK: {e}")
            raise InvalidCIKException(f"Invalid CIK: {e}")

        url = f"{self.DATA_URL}/api/xbrl/companyconcept/CIK{cik_obj}/{taxonomy}/{tag}.json"
        self.logger.info(f"Making request to: {url}")
        response = await self._make_request(url)

        return self._parse_response_json(response)

    async def get_company_facts(self, cik: str) -> Dict[str, Any]:
        cik_obj = CIK(cik)
        try:
            cik_obj.verify_cik()
        except ValueError as e:
            self.logger.error(f"Invalid CIK: {e}")
            raise InvalidCIKException(f"Invalid CIK: {e}")

        url = f"{self.DATA_URL}/api/xbrl/companyfacts/CIK{cik_obj}.json"
        self.logger.info(f"Making request to: {url}")
        response = await self._make_request(url)

        return self._parse_response_json(response)

    async def get_frames(self, period: str) -> Dict[str, Any]:
        period_obj = Period(period)
        try:
            period_obj.is_valid()
        except ValueError as e:
            self.logger.error(f"Invalid period: {e}")
            raise ValueError(f"Invalid period: {e}")

        url = f"{self.DATA_URL}/api/xbrl/frames/us-gaap/AccountsPayableCurrent/USD/{period_obj}.json"
        self.logger.info(f"Making request to: {url}")
        response = await self._make_request(url)

        return self._parse_response_json(response)

    async def download_company_facts(self, file_path: str | Path, unzip: bool = False) -> None:
        url = f"{self.BASE_URL}/Archives/edgar/daily-index/xbrl/companyfacts.zip"
        await self._download_file(url=url, file_path=file_path, unzip=unzip)

    async def download_filing_history(self, file_path: str | Path, unzip: bool = False) -> None:
        url = f"{self.BASE_URL}/Archives/edgar/daily-index/bulkdata/submissions.zip"
        await self._download_file(url=url, file_path=file_path, unzip=unzip)

    async def company_tickers(self) -> Dict[str, Any]:
        url = f"{self.BASE_URL}/files/company_tickers.json"
        self.logger.info(f"Making request to: {url}")
        response = await self._make_request(url)
        return self._parse_response_json(response)

    async def get_ash_file(self, cik: str, ) -> None:
        cik_obj = CIK(cik)
        try:
            cik_obj.verify_cik()
        except ValueError as e:
            self.logger.error(f"Invalid CIK: {e}")
            raise InvalidCIKException(f"Invalid CIK: {e}")

        url = f"{self.BASE_URL}/Archives/edgar/daily-index/{cik_obj}/sub.txt"
        await self._download_file(url=url, file_path=file_path, unzip=unzip)
