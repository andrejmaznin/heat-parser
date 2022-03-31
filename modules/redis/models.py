from datetime import datetime
from typing import Optional

import country_converter
from redis_om import JsonModel

from parsing.consts import currents


class _BaseModel(JsonModel):
    class Config:
        orm_mode = True


class Country(_BaseModel):
    iso_code: str

    @property
    def name(self):
        return country_converter.convert([self.iso_code], to='name')


class Domain(_BaseModel):
    address: str
    country: Optional[Country] = None


class ParsedPath(_BaseModel):
    domain: str
    path: Optional[str] = None


class ParsedInstance(_BaseModel):
    date_parsed: datetime = datetime.now()
    domain: str = currents.get_domain()
    url: str = currents.get_url()


class PhoneNumber(ParsedInstance):
    number: str
    country: Country


class Email(ParsedInstance):
    email: str

    @property
    def email_domain(self) -> Domain:
        return Domain(address=self.email.split('@')[-1])


class PersonName(ParsedInstance):
    forename: str
    surname: str


class QuotedName(ParsedInstance):
    value: str
    language: Optional[str]
