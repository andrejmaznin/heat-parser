from bs4 import BeautifulSoup

from parsing.internal import parse_source


def run_parsers(source: BeautifulSoup) -> dict:
    return parse_source(source)
