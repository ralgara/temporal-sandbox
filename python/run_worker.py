import asyncio
import os
import pdb
import sys

from temporalio import activity, workflow
from temporalio.client import Client, TLSConfig
from temporalio.worker import Worker

from activities import *
from workflows import *
import database

async def main():
    print(f"Starting worker [{os.environ['TEMPORAL_WORKER_ROLE']}]")
    server_addr = os.getenv('TEMPORAL_SERVER')
    if server_addr is None:
        print("$TEMPORAL_SERVER is required but undefined")
        sys.exit(1)
    print(f"Connecting to Temporal server at {server_addr}")
    client = await Client.connect(server_addr, namespace="default")
    database.initialize()
    print(f"Connected to server [{client.identity}]")
    print("----------------")
    if 'TEMPORAL_WORKER_ROLE' in os.environ:
        if os.environ['TEMPORAL_WORKER_ROLE'] == 'pageviews':
            queue="wikipedia-pageviews"
            print(f"Starting pageviews worker [{queue}]")
            w = Worker(
                client, 
                task_queue = queue,
                workflows = None,
                activities = [get_pageviews],
                #max_activities_per_second = 3
            )
        elif os.environ['TEMPORAL_WORKER_ROLE'] == 'article':
            queue="wikipedia-article"
            print(f"Starting article worker [{queue}]")
            w = Worker(
                client, 
                task_queue=queue,
                workflows = None,
                activities=[get_article],
                #max_activities_per_second = 3
            )
        elif os.environ['TEMPORAL_WORKER_ROLE'] == 'filter':
            queue="wikipedia-filter"
            print(f"Starting filter worker [{queue}]")
            w = Worker(
                client, 
                task_queue=queue,
                workflows = None,
                activities=[filter_articles])
        elif os.environ['TEMPORAL_WORKER_ROLE'] == 'workflow-download':
            queue="wikipedia-pageviews"
            print(f"Starting workflow worker [{queue}]")
            w = Worker(
                client, 
                task_queue=queue,
                workflows = [WikipediaPageviews],
                activities=None)
        elif os.environ['TEMPORAL_WORKER_ROLE'] == 'workflow-import':
            queue="wikipedia-import-pageviews"
            print(f"Starting workflow worker [{queue}]")
            w = Worker(
                client, 
                task_queue=queue,
                workflows = [WikipediaImportPageviews],
                activities=None)            
        elif os.environ['TEMPORAL_WORKER_ROLE'] == 'helo':
            queue="wikipedia-helo"
            print(f"Starting helo worker [{queue}]")
            w = Worker(
                client, 
                task_queue = queue,
                workflows = [Helo],
                activities = [get_pageviews, get_article],
            )
        else:
            print(f"Invalid value in $TEMPORAL_WORKER_ROLE: {os.environ['TEMPORAL_WORKER_ROLE']}")
            sys.exit(1)
        await w.run()

    else:
        print(f"Required $TEMPORAL_WORKER_ROLE is undefined")
        sys.exit(1)


if __name__ == "__main__":
    print("----------------------")
    print(f"{sys.argv}")
    print("----------------------")
    asyncio.run(main())

            