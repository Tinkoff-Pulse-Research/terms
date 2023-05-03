import json
from pprint import pprint

import requests
from bs4 import BeautifulSoup

with open("glossary.json", 'r', encoding='utf-8') as f:
    glossary = json.load(f)


def get_page(url: str) -> str:
    return requests.get(url).text


def get_terms(page: str) -> dict:
    soup = BeautifulSoup(page, 'html.parser')
    sections = soup.find_all("div", class_='more')
    terms = [term.text.strip().split("\r\n")[0] for term in sections]
    definitions = ["".join(term.text.strip().split("\r\n")[1:]).strip() for term in sections]
    return dict(zip(terms, definitions))


if __name__ == '__main__':
    terms = get_terms(get_page("https://iva.partners/blog/birzhevoisleng"))
    # pprint(terms)
    for term in terms:
        if not glossary.get(term, None):
            glossary[term] = terms[term]

    with open("glossary.json", 'w', encoding='utf-8') as f:
        json.dump(glossary, f, ensure_ascii=False, indent=4)
