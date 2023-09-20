import asyncio

from temporalio import activity, workflow
from temporalio.client import Client, TLSConfig
from temporalio.worker import Worker

from activities import get_pageviews, get_article, say_hello, square, increment, halve
from workflows import WikipediaPageviews, SayHello, Transform

async def main_transform():
    # client = await Client.connect("localhost:7233", namespace="default")
    with open("/Users/ralgara/code/temporal-sandbox/client-cert.pem", "rb") as certFile:
        client_cert = certFile.read()

    with open("/Users/ralgara/code/temporal-sandbox/client-private-key.pem", "rb") as privateKeyFile:
        client_private_key = privateKeyFile.read()

    # Start client
    client = await Client.connect("enrichments-testing-b1.11a66.tmprl.cloud:7233",
                                  namespace="enrichments-testing-b1.11a66",
                                  tls=TLSConfig(client_cert=client_cert, 
                                  client_private_key=client_private_key))
    worker = Worker(
        client, 
        task_queue = "repro",
        #task_queue="transform-queue",
        # workflows=[Transform], 
        activities=[square, increment, halve]

    )

    # await worker.run()
    await worker.stop()

async def main_wikipedia():
    print("Starting main_wikipedia worker")
    client = await Client.connect("localhost:7233", namespace="default")
    print("Connected to server")
    w2 = Worker(
        client, 
        task_queue="wikipedia-pageviews-queue",  
        workflows=[WikipediaPageviews],
        activities=[get_pageviews, get_article]
    )  
    await w2.run()


if __name__ == "__main__":
    #asyncio.run(main_hello())
    asyncio.run(main_wikipedia())
    #asyncio.run(main_transform())
            