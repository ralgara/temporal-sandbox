from datetime import timedelta
from temporalio import workflow
from temporalio.common import RetryPolicy

# Import activity, passing it through the sandbox without reloading the module
with workflow.unsafe.imports_passed_through():
    from activities import *
    
@workflow.defn
class WikipediaPageviews:
    @workflow.run
    async def run(self, date: str) -> str:
        print(f"WikipediaPageviews.run({date})")
        articles = await workflow.execute_activity(
            get_pageviews, 
            date,
            task_queue = "wikipedia-pageviews",
            start_to_close_timeout=timedelta(seconds=10)
        )
        print(articles)
        filtered_articles = await workflow.execute_activity(
            "filter_articles", 
            articles,
            task_queue = "wikipedia-filter",
            start_to_close_timeout=timedelta(seconds=10)    
        )
        for article in filtered_articles:
            print(f"article: [{article}")
            workflow.start_activity(
                get_article, 
                article['article'],
                task_queue = "wikipedia-article",
                start_to_close_timeout=timedelta(seconds=10)
            )
        return "Done"
        