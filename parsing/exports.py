from bs4 import BeautifulSoup

from parsing.parsers import parse_source


def run_parsers(source: BeautifulSoup, url: str) -> dict:
    return parse_source(source, url)
