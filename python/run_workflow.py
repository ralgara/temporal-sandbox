import asyncio
import datetime
import database
import os
import sys

from run_worker import WikipediaPageviews, WikipediaImportPageviews

from temporalio.client import Client

async def get_client():
    print(f"Starting worker [{os.environ['TEMPORAL_WORKER_ROLE']}]")
    server_addr = os.getenv('TEMPORAL_SERVER')
    if server_addr is None:
        print("$TEMPORAL_SERVER is required but undefined")
        sys.exit(1)
    print(f"Connecting to Temporal server at {server_addr}")
    client = await Client.connect(server_addr, namespace="default")

    # with open("/Users/ralgara/code/temporal-sandbox/client-cert.pem", "rb") as certFile:
    #     client_cert = certFile.read()

    # with open("/Users/ralgara/code/temporal-sandbox/client-private-key.pem", "rb") as privateKeyFile:
    #     client_private_key = privateKeyFile.read()
    print(f"Connected to server [{client.identity}]")
    return client

async def main_wikipedia_download():
    client = await get_client()
    start_date = datetime.date(2016,1,1)
    end_date = datetime.date(2023,10,15)
    date_range = [
        start_date + datetime.timedelta(days=x) 
        for x in range(0, (end_date - start_date).days)
    ]
    print(f"Looping over date range [{date_range}]")
    for d in date_range:

        print(f"Starting workflow {d}")

        id = f"wikipedia-pageviews-{d}"

        result = await client.execute_workflow(
            WikipediaPageviews.run,
            str(d),
            id = id,
            task_queue="wikipedia-pageviews"
        )

        print(f"Finished running workflow {id}")

async def main_wikipedia_import():
    client = await get_client()
    print("Scanning cache")
    for name, doc in database.get_pageviews_generator():
        id = f"wikipedia-import-pageviews-{name}"
        print(f"Starting {id}")
        
        result = await client.execute_workflow(
            WikipediaImportPageviews.run,
            doc,
            id = id,
            task_queue="wikipedia-import-pageviews"
        )

        print(f"Finished running workflow {id}")



if __name__ == "__main__":
    print("----------------------")
    print(f"{sys.argv}")
    print("----------------------")

    role = os.environ['TEMPORAL_WORKER_ROLE']
    if role == 'workflow-download':
        asyncio.run(main_wikipedia_download())
    elif role == 'workflow-import':
        asyncio.run(main_wikipedia_import())
    else:
        print(f"Workflow '{role}' is not defined")
        sys.exit(1)


