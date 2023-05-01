import json
from pprint import pprint

import requests
from bs4 import BeautifulSoup

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6,zh;q=0.5',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Host': 'itinvest.ru',
    'Pragma': 'no-cache',
    'sec-ch-ua': 'Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform' "'Windows"',Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
}


def get_page(url: str) -> str:
    """Returning a HTML code of url"""
    return requests.get(
        url,
        headers=headers
    ).text


def get_terms(page: str) -> list:
    """Returning a list of terms"""
    soup = BeautifulSoup(page, "html.parser")
    return soup.find_all("a", class_="dictionary-wrapper__item-word")


def get_definition(term_url: str) -> str:
    """Returning a definition of provided term"""
    page = get_page(f"https://itinvest.ru{term_url}")
    soup = BeautifulSoup(page, "html.parser")
    return soup.find("div", class_="dictionary-wrapper dictionary-wrapper__detail").text.strip()


if __name__ == '__main__':
    page = get_page("https://itinvest.ru/education12/glossary/")
    terms = get_terms(page)
    result = {}
    for i, term in enumerate(terms):
        try:
            print(f"Processing {i + 1}/{len(terms)} ({term.text})")
            result[term.text] = get_definition(term.attrs['href'])
        except Exception as e:
            print(f"[ERROR] {e}")
    with open("glossary.json", 'r') as f:
        json.dump(result, f, indent=4, encodings='utf-8')
