from datetime import datetime
from typing import Dict, List

import pymorphy2
from bs4 import BeautifulSoup
from dateutil.parser import parse as parse_date
from langdetect import detect as detect_language

from modules.redis.models import (Email, ParsedInstance, PersonName,
                                  PhoneNumber, QuotedName)
from parsing.consts import (EMAIL_REGEX, PERSON_NAME_REGEX, PHONE_NUMBER_REGEX,
                            QUOTED_NAME_REGEX, currents)
from parsing.registry import parsers, register
from parsing.utils import (check_text, find_person_names, format_quotes,
                           is_date, parse_numbers)

morph = pymorphy2.MorphAnalyzer()
state = {}


@register(PhoneNumber)
def parse_numbers_from_source(source: BeautifulSoup) -> List[PhoneNumber]:
    numbers = source.find_all(text=PHONE_NUMBER_REGEX)
    parsed_numbers = []
    for number in numbers:
        parsed_numbers += parse_numbers(number)

    return parsed_numbers


@register(Email)
def parse_emails_from_source(source: BeautifulSoup) -> List[Email]:
    emails = [
        Email(
            email=element.text.strip(),
            **currents.get_currents()
        ).save() for element in source.find_all(text=EMAIL_REGEX)
    ]

    return emails


# @register('dates')
def parse_dates_from_source(source: BeautifulSoup) -> List[datetime]:
    dates = source.find_all(text=lambda a: is_date(a))
    return [parse_date(date) for date in dates]


@register(PersonName)
def parse_names_from_source(source: BeautifulSoup) -> List[PersonName]:
    names = []
    for element in source.find_all(text=PERSON_NAME_REGEX):
        names += find_person_names(element.text)

    return names


@register(QuotedName)
def parse_quoted_names_from_source(source: BeautifulSoup) -> List[QuotedName]:
    raw_texts = [element.text
                 for element in source.find_all(text=QUOTED_NAME_REGEX)]
    quoted_names = []

    for text in raw_texts:
        text = format_quotes(text).split("'")[1::2]
        quoted_names += [noun for noun in text
                         if noun not in quoted_names and check_text(noun)]

    parsed_nouns = [
        QuotedName(
            value=morph.parse(noun)[0].normal_form.capitalize(),
            language=detect_language(noun),
            **currents.get_currents()
        ).save()
        for noun in quoted_names
    ]

    return parsed_nouns


def parse_source(
    source: BeautifulSoup,
    url: str
) -> Dict[ParsedInstance, List]:
    currents.domain, currents.url = url.split('//', 1)[-1].split('/', 1)

    return {name: value(source) for name, value in parsers.items()}
