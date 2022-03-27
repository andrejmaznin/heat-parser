from datetime import datetime
from typing import Dict, List

import pymorphy2
from bs4 import BeautifulSoup
from dateutil.parser import parse as parse_date
from phonenumbers import PhoneNumberMatcher

from parsing.consts import (EMAIL_REGEX, PERSON_NAME_REGEX, PHONE_NUMBER_REGEX,
                            QUOTED_NAME_REGEX)
from parsing.service import parsers, register

morph = pymorphy2.MorphAnalyzer()


def parse_numbers(text: str) -> List[str]:
    return [match.raw_string for match in PhoneNumberMatcher(text, None)]


def is_date(timestr: str) -> bool:
    try:
        parse_date(timestr)
        return True
    except (ValueError, OverflowError):
        return False


def parse_numbers_from_source(source: BeautifulSoup) -> List[str]:
    numbers = source.find_all(text=PHONE_NUMBER_REGEX)
    parsed_numbers = []
    for number in numbers:
        parsed_numbers += parse_numbers(number)
    return parsed_numbers


def format_quotes(text: str) -> str:
    text = text.replace('«', '"')
    text = text.replace('»', '"')
    return text


# should be replaced with regex
def check_text(text: str) -> bool:
    if text == text.capitalize() and len(text) <= 15 and text.count(' ') <= 1:
        return True
    return False


@register('emails')
def parse_emails_from_source(source: BeautifulSoup) -> List[str]:
    emails = [element.text.strip() for element in
              source.find_all(text=EMAIL_REGEX)]
    return emails


# @register('dates')
def parse_dates_from_source(source: BeautifulSoup) -> List[datetime]:
    dates = source.find_all(text=lambda a: is_date(a))

    return [parse_date(date) for date in dates]


@register('names')
def parse_names_from_source(source: BeautifulSoup) -> List[str]:
    names = [
        element.text for element in
        source.find_all(text=PERSON_NAME_REGEX)
    ]
    return names


@register('nouns')
def parse_proper_nouns_from_source(source: BeautifulSoup) -> List[str]:
    raw_texts = [element.text
                 for element in source.find_all(text=QUOTED_NAME_REGEX)]
    parsed_nouns = []
    for text in raw_texts:
        nouns = format_quotes(text).split('"')[1::2]
        parsed_nouns += [noun for noun in nouns
                         if noun not in parsed_nouns and check_text(noun)]
    parsed_nouns = [morph.parse(noun)[0].normal_form.capitalize()
                    for noun in parsed_nouns]

    return parsed_nouns


def parse_source(source: BeautifulSoup) -> Dict[str, List]:
    return {name: value(source) for name, value in parsers.items()}
