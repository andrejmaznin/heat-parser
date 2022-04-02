import re
from typing import List

import bs4
import requests


def parser_site_from_explorer(site_link: str) -> List[str]:
    try:
        # User agent
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.121 Safari/537.36' # noqa
        }

        r = requests.get(f'{site_link}', headers=headers)
        # Html code from site
        html_text = r.text

        soup = bs4.BeautifulSoup(html_text, 'html.parser')
        # scraping
        links = soup.find_all('a')

        array_links = []
        for item in links:
            link = re.match(r'(https?://[\S]+)', item.get('href'))
            if link is None:
                continue
            else:
                array_links.append(link.group(0))
        return array_links

    except requests.exceptions.InvalidSchema:
        print('Такой страницы нет')


if __name__ == '__main__':
    # Example
    links = parser_site_from_explorer(
        'https://docs.python-requests.org/en/latest/index.html'
    )
    for link in links:
        print(link)
