import re
from typing import List

from dateutil.parser import parse as parse_date
from phonenumbers import PhoneNumberMatcher
from phonenumbers.phonenumberutil import region_code_for_country_code

from modules.redis.models import Country, PersonName, PhoneNumber
from parsing.consts import PERSON_NAME_REGEX, currents


def parse_numbers(text: str) -> List[str]:
    return [
        PhoneNumber(
            number=match.raw_string.replace(' ', ''),
            country=Country(
                iso_code=region_code_for_country_code(
                    match.number.country_code
                )
            ),
            **currents.get_currents()
        ).save().pk for match in PhoneNumberMatcher(text, None)
    ]


def is_date(timestr: str) -> bool:
    try:
        parse_date(timestr)
        return True
    except (ValueError, OverflowError):
        return False


def format_quotes(text: str) -> str:
    text = text.replace('«', "'")
    text = text.replace('»', "'")
    text = text.replace('"', "'")
    return text


def find_person_names(text: str) -> List[str]:
    names = []

    for name in re.findall(PERSON_NAME_REGEX, text):
        forename, surname = name.split()
        names.append(
            PersonName(
                forename=forename,
                surname=surname,
                **currents.get_currents()
            ).save().pk
        )

    return names


# should be replaced with regex
def check_text(text: str) -> bool:
    return text == text.capitalize() and text.count(' ') <= 1 and text
