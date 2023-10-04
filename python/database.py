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
    run_query("CREATE TABLE dates (date, status)")

def cached_download(path: str, url: str) -> bool:
    cache_path = f"{os.getcwd()}/cache/{path}"
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

