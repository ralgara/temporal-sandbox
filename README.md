# temporal-sandbox

Temporary repo for discussion with Temporal team. Objective: demo cross-language activities within a single workflow.

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
