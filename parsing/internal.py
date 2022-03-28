from typing import List

import pymorphy2
from dateutil.parser import parse as parse_date
from phonenumbers import PhoneNumberMatcher

morph = pymorphy2.MorphAnalyzer()


def parse_numbers(text: str) -> List[str]:
    return [match.raw_string for match in PhoneNumberMatcher(text, None)]


def is_date(timestr: str) -> bool:
    try:
        parse_date(timestr)
        return True
    except (ValueError, OverflowError):
        return False


def format_quotes(text: str) -> str:
    text = text.replace('«', '"')
    text = text.replace('»', '"')
    return text


# should be replaced with regex
def check_text(text: str) -> bool:
    if text == text.capitalize() and len(text) <= 15 and text.count(' ') <= 1:
        return True
    return False
