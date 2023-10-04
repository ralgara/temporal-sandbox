import asyncio
import datetime

from run_worker import WikipediaPageviews

from temporalio.client import Client

async def get_client():
    print("Connecting to Temporal server")
    return await Client.connect("localhost:7233")

async def main_wikipedia():
    client = await get_client()
    start_date = datetime.date(2016,1,1)
    end_date = datetime.date(2023,10,4)
    date_range = [
        start_date + datetime.timedelta(days=x) 
        for x in range(0, (end_date - start_date).days)
    ]
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

if __name__ == "__main__":
    asyncio.run(main_wikipedia())


