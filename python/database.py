import json
import os
import requests
import time
import sqlite3

class DownloadError(RuntimeError):
    def __init__(self, status, message):
        self.message = message
        self.status = status
    def __str__(self):
        return f"{self.status}: {self.message}"

def get_cursor():
    con = sqlite3.connect("pageviews.db")
    return con.cursor()

def run_query(query):
    cur = get_cursor()
    return cur.execute(query)

def initialize():
    try:
        run_query("CREATE TABLE IF NOT EXISTS dates (date, status)")
    except Exception as e:
        print(e)
    for dir in ('pageviews','articles'):
        os.makedirs(f'cache/{dir}', mode = 0o777, exist_ok = True) 

CACHE_ROOT_DIR=f"{os.getcwd()}/../cache"

def cached_download(path: str, url: str) -> bool:
    cache_path = f"{CACHE_ROOT_DIR}/{path}"
    if not os.path.isfile(cache_path):
        print(f"Missed cache. Downloading {url}")
        headers = {
            'User-Agent': 'ralgara@gmail.com'
        }
        time.sleep(0.5)
        req = requests.request("GET", url, headers=headers)
        if req.ok:
            with open(cache_path, 'w') as cache_file:
                cache_file.write(req.text)
            print("Download cached")  
        else:
            raise DownloadError(status=req.status_code, message=f"Unable to download [{req.text}]")

    with open(cache_path, 'r') as cache_file:
        print(f"Reading from filesystem: {cache_path}")
        return cache_file.read()

def get_pageviews_generator():
    cache_path = f"{CACHE_ROOT_DIR}/pageviews"
    for name, filename in [(f, f"{cache_path}/{f}") for f in os.listdir(cache_path)]:
        with open(filename) as fd:
            print(f"Reading {name} from {filename}")
            pageviews_doc = json.load(fd)
            yield (name, pageviews_doc)