import asyncio

from temporalio import activity, workflow
from temporalio.client import Client, TLSConfig
from temporalio.worker import Worker

from activities import get_pageviews, get_article
from workflows import WikipediaPageviews

async def main_wikipedia():
    print("Starting main_wikipedia worker")
    client = await Client.connect("localhost:7233", namespace="default")

    # with open("/Users/ralgara/code/temporal-sandbox/client-cert.pem", "rb") as certFile:
    #     client_cert = certFile.read()

    # with open("/Users/ralgara/code/temporal-sandbox/client-private-key.pem", "rb") as privateKeyFile:
    #     client_private_key = privateKeyFile.read()
    
    print("Connected to server")
    w2 = Worker(
        client, 
        task_queue="wikipedia-pageviews-queue",  
        workflows=[WikipediaPageviews],
        activities=[get_pageviews, get_article]
    )  
    await w2.run()


if __name__ == "__main__":
    asyncio.run(main_wikipedia())

            