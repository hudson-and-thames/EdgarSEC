from pydantic import BaseModel, Field
from typing import List, Optional


class Address(BaseModel):
    street1: str
    street2: Optional[str]
    city: str
    stateOrCountry: str
    zipCode: str
    stateOrCountryDescription: str


class FormerName(BaseModel):
    name: str
    from_date: Optional[str] = Field(..., alias='from')
    to_date: Optional[str] = Field(..., alias='to')


class FilingsRecent(BaseModel):
    accessionNumber: List[str]


class Filings(BaseModel):
    recent: FilingsRecent


class CompanyFilings(BaseModel):
    cik: str
    entityType: str
    sic: str
    sicDescription: str
    insiderTransactionForOwnerExists: int
    insiderTransactionForIssuerExists: int
    name: str
    tickers: List[str]
    exchanges: List[str]
    ein: str
    description: Optional[str]
    website: Optional[str]
    investorWebsite: Optional[str]
    category: str
    fiscalYearEnd: str
    stateOfIncorporation: str
    stateOfIncorporationDescription: str
    addresses: dict[str, Address]
    phone: str
    flags: Optional[str]
    formerNames: List[FormerName]
    filings: Filings
