from typing import List, Optional

from pydantic import BaseModel


class Country(BaseModel):
    countries: List[str]

    class Config:
        json_schema_extra = {
            "example": {
                "countries": ["turkey", "india"],
            }
        }


class University(BaseModel):
    country: Optional[str] = None
    web_pages: List[str] = []
    name: Optional[str] = None
    alpha_two_code: Optional[str] = None
    domains: List[str] = []


class CountryResponse(BaseModel):
    id: int
    name: str
    alpha_two_code: str
    universities: Optional[List[str]]

    class Config:
        from_attributes = True
