from datetime import timedelta
from temporalio import workflow
from temporalio.common import RetryPolicy

# Import activity, passing it through the sandbox without reloading the module
with workflow.unsafe.imports_passed_through():
    from activities import say_hello
    from activities import get_pageviews, get_article
    from activities import square, increment, halve

@workflow.defn
class Transform:
    @workflow.run
    async def run(self, x:int) -> int:
        x1 = await workflow.execute_activity(
          square,
          x,
          start_to_close_timeout=timedelta(seconds=5)
        )
        x2 = await workflow.execute_activity(
          increment,
          x1,
          start_to_close_timeout=timedelta(seconds=5)
        )
        x3 = await workflow.execute_activity(
          halve,
          x,
          start_to_close_timeout=timedelta(seconds=5)
        )


@workflow.defn
class SayHello:
    @workflow.run
    async def run(self, name: str) -> str:
        return await workflow.execute_activity(
            say_hello, 
            name, 
            start_to_close_timeout=timedelta(seconds=5)
        )
    
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
                article['article'], 
                start_to_close_timeout=timedelta(seconds=10),
                retry_policy=RetryPolicy(
                    maximum_attempts=1,
                    # non_retryable_error_types=["ValueError"],
                )
            )
        return "Done"
        
