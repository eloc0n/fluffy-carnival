from typing import List, Optional
from sqlalchemy.dialects.postgresql import ARRAY
from sqlmodel import Field, Relationship, SQLModel  # type: ignore


"""
Expected payload format from service.

{
  "turkey": [
        {
        "country": "Turkey",
        "web_pages": [
                "https://kyrenia.edu.tr"
            ],
        "name": "University of Kyrenia",
        "alpha_two_code": "TR",
        "domains": [
                "std.kyrenia.edu.tr",
                "kyrenia.edu.tr"
            ]
        },
    ]
}
"""


# Country model
class Country(SQLModel, table=True):
    __tablename__ = "countries"

    id: int = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    alpha_two_code: str = Field(unique=True)

    # Relationship to University
    universities: List["University"] = Relationship(back_populates="country")


# University model
class University(SQLModel, table=True):
    __tablename__ = "universities"

    id: int = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    country_id: int = Field(foreign_key="countries.id")

    # Relationship to Country
    country: Country = Relationship(back_populates="universities")

    # Use ARRAY field to store lists of web pages and domains
    web_pages: Optional[List[str]] = Field(default=[], sa_column=ARRAY)
    domains: Optional[List[str]] = Field(default=[], sa_column=ARRAY)
