import asyncio
import datetime


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
            "WikipediaPageviews",
            date,
            id = id,
            task_queue="wikipedia-pageviews-queue"
        )

        print(f"Finished running workflow {id}")

if __name__ == "__main__":
    #asyncio.run(main_transform())
    # asyncio.run(main_hello())
    asyncio.run(main_wikipedia())


