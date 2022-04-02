import re
from asyncio import gather
from datetime import datetime
from typing import List

import aiohttp
import pymorphy2
from aiohttp import ClientError
from bs4 import BeautifulSoup
from dateutil.parser import parse as parse_date
from langdetect import detect as detect_language

from modules.redis.models import (Email, ParsedUrl, PersonName, PhoneNumber,
                                  QuotedName)
from parsing.consts import (EMAIL_REGEX, PERSON_NAME_REGEX, PHONE_NUMBER_REGEX,
                            PROTOCOL, QUOTED_NAME_REGEX, currents)
from parsing.registry import parsers, register
from parsing.utils import (check_text, find_person_names, format_quotes,
                           is_date, parse_numbers)

morph = pymorphy2.MorphAnalyzer()
state = {}


def parse_urls_from_source(
    source: BeautifulSoup,
    domain: str = None,
    ignore_local: bool = True
) -> List[ParsedUrl]:
    hrefs: List[str] = [a['href'] for a in source.find_all('a', href=True)]
    parsed_urls = [
        ParsedUrl(
            url=href,
            same_domain='true'
            if href.startswith('/') else None,  # pointing to the same domain
            **currents.get_currents()
        ).save() for href in hrefs if (domain in href) != ignore_local
    ]
    print([result.url for result in parsed_urls])

    return parsed_urls


@register(PhoneNumber)
def parse_numbers_from_source(source: BeautifulSoup) -> List[PhoneNumber]:
    numbers = source.find_all(text=PHONE_NUMBER_REGEX)
    parsed_numbers = []
    for number in numbers:
        parsed_numbers += parse_numbers(number)

    return parsed_numbers


@register(Email)
def parse_emails_from_source(source: BeautifulSoup) -> List[str]:
    parsed_emails = []
    for element in source.find_all(text=EMAIL_REGEX):
        parsed_emails += [
            Email(
                email=email.strip(),
                **currents.get_currents()
            ).save().pk for email in re.findall(EMAIL_REGEX, element.text)
        ]

    return parsed_emails


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
def parse_quoted_names_from_source(source: BeautifulSoup) -> List[str]:
    raw_texts = [element.text
                 for element in source.find_all(text=QUOTED_NAME_REGEX)]
    quoted_names = []

    for text in raw_texts:
        text = format_quotes(text).split("'")[1::2]
        quoted_names += [
            noun for noun in text
            if noun not in quoted_names and check_text(noun)
        ]

    parsed_nouns = []
    for noun in quoted_names:
        parsed_nouns.append(
            QuotedName(
                value=morph.parse(noun)[0].normal_form.capitalize(),
                language=detect_language(noun),
                **currents.get_currents()
            ).save().pk
        )

    return parsed_nouns


def parse_source(
    source: BeautifulSoup,
    url: str,
    ignore_local: bool = True
) -> List[ParsedUrl]:
    domain, path = url.split('//', 1)[-1].split('/', 1)
    currents.domain, currents.path = domain, path

    parsed_urls = parse_urls_from_source(
        source=source,
        domain=domain,
        ignore_local=ignore_local
    )

    for parser in parsers.values():
        parser(source)

    return parsed_urls


async def parse_recursive(entrypoint: str, depth: int = 1, ignore_local=True):
    if depth == 0 or not entrypoint.startswith('http'):
        return
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(entrypoint) as response:
                source = BeautifulSoup(await response.text())
    except ClientError:
        return

    urls = parse_source(source=source, url=entrypoint)

    depth = depth - 1 if depth > 0 else depth
    return await gather(
        *[
            parse_recursive(
                entrypoint=PROTOCOL + url.domain_found + url.url
                if url.same_domain else url.url,
                depth=depth
            ) for url in urls
        ]
    )
