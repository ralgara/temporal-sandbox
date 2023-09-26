from temporalio import activity
from database import cached_download
import json
import os
import requests
import datetime
import pdb

@activity.defn
async def get_pageviews(date: str) -> list:
    print(f"get_pageviews({date})")
    url_prefix = "https://wikimedia.org/api/rest_v1/metrics/pageviews/top/en.wikipedia/all-access/"
    url = url_prefix + date.replace('-','/')
    path = f"pageviews/{date.replace('-','')}"
    print(activity.info())
    doc = json.loads(cached_download(path, url))
    return doc['items'][0]['articles'][:10]

@activity.defn
async def filter_articles(articles: list[dict]) -> list:
    print(f"filter_articles()")
    return articles[:10]

@activity.defn
async def get_article(title: str) -> str:
    print(f"get_article({title})")
    url = "https://en.wikipedia.org/w/api.php?" + \
        "action=query&" + \
        "prop=revisions&" + \
        f"titles={title}&" + \
        "rvslots=*&" + \
        "rvprop=content&" + \
        "formatversion=2&" + \
        "format=json"

    headers = {
        'User-Agent': 'ralgara@gmail.com'
    }
    path = f"articles/{title}"
    content = cached_download(path, url)
    doc = json.loads(content)
    return content[:500]



