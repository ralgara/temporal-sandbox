from temporalio import activity
from database import DownloadError, cached_download, get_pageviews_generator
import json
import os
import requests
import datetime
import pdb

@activity.defn
async def import_pageviews(doc: dict) -> str:
    print(f"import_pageviews({date})")
    url_prefix = "https://wikimedia.org/api/rest_v1/metrics/pageviews/top/en.wikipedia/all-access/"
    url = url_prefix + date.replace('-','/')
    path = f"pageviews/{date.replace('-','')}"
    s = cached_download(path, url)
    doc = json.loads(s)
    return doc['items'][0]['articles'][:10]

@activity.defn
async def get_pageviews(date: str) -> list[dict]:
    print(f"get_pageviews({date})")
    url_prefix = "https://wikimedia.org/api/rest_v1/metrics/pageviews/top/en.wikipedia/all-access/"
    url = url_prefix + date.replace('-','/')
    path = f"pageviews/{date.replace('-','')}"
    s = cached_download(path, url)
    doc = json.loads(s)
    return doc['items'][0]['articles'][:10]

@activity.defn
async def get_article(title: str) -> str:
    url = "https://en.wikipedia.org/w/api.php?" + \
        "action=query&" + \
        "prop=revisions&" + \
        f"titles={title}&" + \
        "rvslots=*&" + \
        "rvprop=content&" + \
        "formatversion=2&" + \
        "format=json"
    print(f"get_article({title}): {url}")

    headers = {
        'User-Agent': 'ralgara@gmail.com'
    }
    path = f"articles/{title}"
    try:
        content = cached_download(path, url)
    except Exception as e:
        return str(e)
    doc = json.loads(content)
    return json.dumps(doc['query']['pages'][0])[:250]


