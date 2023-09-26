import asyncio
import datetime

from run_worker import SayHello
from run_worker import WikipediaPageviews
from run_worker import Transform

from temporalio.client import Client

async def get_client():
    print("Connecting to Temporal server")
    return await Client.connect("localhost:7233")

async def main_wikipedia():
    client = await get_client()
    start_date = datetime.datetime.today()
    for i in range(4):
        
        date = str(
            (
                start_date - datetime.timedelta(days=i+7)
            ).date()
        )

        print(f"Starting workflow {date}")

        id = f"wikipedia-pageviews-{date}"

        result = await client.execute_workflow(
            WikipediaPageviews.run,
            date,
            id = id,
            task_queue="wikipedia-pageviews"
        )

        print(f"Finished running workflow {id}")

if __name__ == "__main__":
    asyncio.run(main_wikipedia())


