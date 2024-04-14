# temporal-sandbox

Temporal demo. Objective: demo cross-language activities within a single workflow. Application is a Wikipedia sampler driven by pageviews, downloading the top N articles. Intended for information trend analysis.

## Quick start
1. Start Temporal server
```
nohup temporal server start-dev &
```

2. Start application stack
```
docker compose up
```


# Requirements
* Python
* Docker
* Go

# Getting started

## Install local Temporal server (optional for development)
...

## About
The application in this repo is a data collection workflow which pulls traffic data (page views) from Wikipedia. The workflow implements this pseudocode:
```
for d in range(dates):
    pv = download_pageviews(wikipedia_api, d)
    for each article in pv (top N):
        page = download(article)
        write_to_database(page)
```
## Running

For local development, this repo provides a docker-compose stack. Use:

```
docker-compose up
```

## Building the Go filter worker

```
export GOPROXY=direct
cd golang/temporal-one
GOOS=linux go build worker.go
```
