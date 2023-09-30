import os
import requests
import sqlite3

def get_cursor():
    con = sqlite3.connect("pageviews.db")
    return con.cursor()

def run_query(query):
    cur = get_cursor()
    return cur.execute(query)

def initialize():
    run_query("CREATE TABLE dates (date, status)")

def cached_download(path: str, url: str) -> bool:
    cache_path = f"{os.getcwd()}/cache/{path}"
    if not os.path.isfile(cache_path):
        print(f"Missed cache. Downloading {url}")
        headers = {
            'User-Agent': 'ralgara@gmail.com'
        }
        req = requests.request("GET", url, headers=headers)
        if req.ok:
            with open(cache_path, 'w') as cache_file:
                cache_file.write(req.text)
            print("Download cached")  
        else:
            raise Exception(f"Unable to download [({req.status_code}) {req.text}]")

    with open(cache_path, 'r') as cache_file:
        print(f"Reading from filesystem: {cache_path}")
        return cache_file.read()

