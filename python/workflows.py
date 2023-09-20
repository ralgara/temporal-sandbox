from datetime import timedelta
from temporalio import workflow
from temporalio.common import RetryPolicy

from activities import get_pageviews, get_article

@workflow.defn
class WikipediaPageviews:
    @workflow.run
    async def run(self, date: str) -> str:
        print(f"WikipediaPageviews.run({date})")
        articles = await workflow.execute_activity(
            get_pageviews, 
            date, 
            start_to_close_timeout=timedelta(seconds=10),
            retry_policy=RetryPolicy(
                maximum_attempts=1,
                # non_retryable_error_types=["ValueError"],
            )
        )
        print('oh no!')
        print('art', articles)

        filtered_articles = await workflow.execute_activity(
            "filter_articles", 
            articles, 
            task_queue="wikipedia-pageviews-queue-golang",
            start_to_close_timeout=timedelta(seconds=10),
            retry_policy=RetryPolicy(
                maximum_attempts=1,
                # non_retryable_error_types=["ValueError"],
            )            
        )
        for article in filtered_articles:
            print(f"article: {article}")
            workflow.start_activity(
                get_article, 
                article, 
                start_to_close_timeout=timedelta(seconds=10),
                retry_policy=RetryPolicy(
                    maximum_attempts=1,
                    # non_retryable_error_types=["ValueError"],
                )
            )
        return "Done"
        
