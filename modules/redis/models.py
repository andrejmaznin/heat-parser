from datetime import datetime
from typing import Optional

import country_converter
from redis_om import EmbeddedJsonModel, Field, HashModel, JsonModel

from parsing.consts import currents


class Country(EmbeddedJsonModel):
    iso_code: str

    @property
    def name(self):
        return country_converter.convert([self.iso_code], to='name')


class Domain(JsonModel):
    address: str = Field(index=True)
    country: Optional[Country] = None


class ParsedInstance:
    date_parsed: datetime = datetime.now()
    domain_found: Optional[str] = None
    path: str = currents.get_url()


class ParsedUrl(ParsedInstance, HashModel):
    url: str
    same_domain: Optional[str] = None


class PhoneNumber(ParsedInstance, JsonModel):
    number: str = Field(index=True)
    country: Country


class Email(ParsedInstance, HashModel):
    email: str

    @property
    def email_domain(self) -> Domain:
        return Domain(address=self.email.split('@')[-1])


class PersonName(ParsedInstance, HashModel):
    forename: str
    surname: str


class QuotedName(ParsedInstance, HashModel):
    value: str
    language: Optional[str]
