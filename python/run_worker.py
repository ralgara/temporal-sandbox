import asyncio

from temporalio import activity, workflow
from temporalio.client import Client
from temporalio.worker import Worker

from activities import get_pageviews, get_article 
from workflows import WikipediaPageviews

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
    asyncio.run(main_wikipedia())
            
