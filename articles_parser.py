import html
import re
from pprint import pprint
from typing import Optional, Tuple

import requests


def get_articles(profile: str = "25cf055b-1543-47a8-b22e-4aa51b124f7b",
                 limit: int = 30, cursor: int = None) -> Optional[Tuple[list, int]]:
    """Returning a tuple of list of articles and next cursor ID."""
    res = requests.get(
        url=f"https://www.tinkoff.ru/api/invest-gw/social/v1/profile/{profile}/post?limit={limit}&cursor={cursor}" if cursor else
        f"https://www.tinkoff.ru/api/invest-gw/social/v1/profile/{profile}/post?limit={limit}"
    )
    data = res.json()
    if data.get("status", None) != 'Ok':
        print(f"[ERROR] {data}")
        return [], None
    return (data['payload']['items'], data['payload']['nextCursor'])


def get_article_text(article_id: str) -> Optional[Tuple[str, str]]:
    """Returning a tuple of article title and content"""
    res = requests.get(
        url=f"https://www.tinkoff.ru/api/invest-gw/social/v1/post/{article_id}"
    )
    data = res.json()
    if data.get("status", None) != 'Ok':
        print(f"[ERROR] {data}")
        return None
    if data['payload']['content']['type'] == 'simple':
        tittle = ""
        text = data['payload']['content']['text']
    else:
        tittle = data['payload']['content']['title']
        text = data['payload']['content']['body']
    return tittle, re.sub(r"(?:\[&|\]|(?:\(https?://.*?\)))", "", re.sub(
        r"\n{2,}",
        "\n",
        html.unescape(
            re.sub(r"(<.*?>)", "", text, flags=re.DOTALL)
        ).replace("\xa0", " ")
    ))


if __name__ == '__main__':
    next_cursor = None
    with open("articles.txt", 'w', encoding='utf-8') as f:
        for _ in range(10):
            articles, cursor = get_articles(cursor=next_cursor)
            for article in articles:
                print(f"Parsing article {article['id']}")
                title, text = get_article_text(article['id'])
                f.write(f"{title}\n\n{text}\n\n\n")
            next_cursor = cursor

# print(get_article_text("b046b6c0-4259-4b6b-a94c-b1ae41c59cc8"))
