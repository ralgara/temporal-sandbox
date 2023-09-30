import asyncio
import datetime

from run_worker import WikipediaPageviews

from temporalio.client import Client

async def get_client():
    print("Connecting to Temporal server")
    return await Client.connect("localhost:7233")

async def main_wikipedia():
    client = await get_client()
    date = datetime.date(2023,9,1) #datetime.datetime.today()
    NDATES=10
    for i in range(NDATES):
        
        date += datetime.timedelta(days=1)

        print(f"Starting workflow {date}")

        id = f"wikipedia-pageviews-{date}"

        result = await client.execute_workflow(
            WikipediaPageviews.run,
            str(date),
            id = id,
            task_queue="wikipedia-pageviews"
        )

        print(f"Finished running workflow {id}")

if __name__ == "__main__":
    asyncio.run(main_wikipedia())


