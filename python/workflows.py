from datetime import timedelta
from temporalio import workflow
from temporalio.common import RetryPolicy

# Import activity, passing it through the sandbox without reloading the module
with workflow.unsafe.imports_passed_through():
    from activities import *
    from time import *

@workflow.defn
class Helo:
    @workflow.run
    async def run(self, page: str) -> dict:
        print(f"Helo.run({page})")
        articles = await workflow.execute_activity(
            get_pageviews, 
            page,
            task_queue = "wikipedia-helo",
            start_to_close_timeout=timedelta(days=1),
            retry_policy=RetryPolicy(
                backoff_coefficient=10,
                maximum_attempts=10,
                initial_interval=timedelta(seconds=1),
                maximum_interval=timedelta(hours=24),
                non_retryable_error_types=["ApplicationError"],
            )
        )        
    
@workflow.defn
class WikipediaPageviews:
    @workflow.run
    async def run(self, date: str) -> dict:
        print(f"WikipediaPageviews.run({date})")
        articles = await workflow.execute_activity(
            get_pageviews, 
            date,
            task_queue = "wikipedia-pageviews",
            start_to_close_timeout=timedelta(days=1),
            retry_policy=RetryPolicy(
                backoff_coefficient=10,
                maximum_attempts=10,
                initial_interval=timedelta(seconds=1),
                maximum_interval=timedelta(hours=24),
                non_retryable_error_types=["DownloadError"],
            )
        )
        filtered_articles = await workflow.execute_activity(
            "filter_articles", 
            articles,
            task_queue = "wikipedia-filter",
            start_to_close_timeout=timedelta(seconds=10)    
        )
        for article in filtered_articles:
            print(f"article: [{article}")
            snippet = await workflow.start_activity(
                get_article, 
                article['article'],
                task_queue = "wikipedia-article",
                start_to_close_timeout=timedelta(seconds=10)
            )
        return {
            "status": "complete",
            "articles": filtered_articles
        }
        