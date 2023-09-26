import asyncio
import os
import pdb
import sys

from temporalio import activity, workflow
from temporalio.client import Client, TLSConfig
from temporalio.worker import Worker

from activities import *
from workflows import *

async def main():
    print(f"Starting activity worker [{os.environ['TEMPORAL_WORKER_ROLE']}]")
    client = await Client.connect("localhost:7233", namespace="default")

    # with open("/Users/ralgara/code/temporal-sandbox/client-cert.pem", "rb") as certFile:
    #     client_cert = certFile.read()

    # with open("/Users/ralgara/code/temporal-sandbox/client-private-key.pem", "rb") as privateKeyFile:
    #     client_private_key = privateKeyFile.read()
    
    print(f"Connected to server [{client.identity}]")
    if 'TEMPORAL_WORKER_ROLE' in os.environ:
        if os.environ['TEMPORAL_WORKER_ROLE'] == 'pageviews':
            queue="wikipedia-pageviews"
            print(f"Starting pageviews worker [{queue}]")
            w = Worker(
                client, 
                task_queue = queue,
                workflows = None,
                activities = [get_pageviews]
            )
        elif os.environ['TEMPORAL_WORKER_ROLE'] == 'article':
            queue="wikipedia-article"
            print(f"Starting pageviews worker [{queue}]")
            w = Worker(
                client, 
                task_queue=queue,
                workflows = None,
                activities=[get_article])
        elif os.environ['TEMPORAL_WORKER_ROLE'] == 'filter':
            queue="wikipedia-filter"
            print(f"Starting filter worker [{queue}]")
            w = Worker(
                client, 
                task_queue=queue,
                workflows = None,
                activities=[filter_articles])            
        elif os.environ['TEMPORAL_WORKER_ROLE'] == 'workflow':
            queue="wikipedia-pageviews"
            print(f"Starting pageviews workflow [{queue}]")
            w = Worker(
                client, 
                task_queue=queue,
                workflows = [WikipediaPageviews],
                activities=None)            
        else:
            print(f"Invalid value in $TEMPORAL_WORKER_ROLE: {os.environ['TEMPORAL_WORKER_ARTICLE']}")
            sys.exit(1)
        
        # pdb.set_trace()
        # print(w.config())
        await w.run()
    else:
        print(f"Required $TEMPORAL_WORKER_ROLE is undefined")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())

            