from temporalio import activity

@activity.defn
async def get_pageviews(date: str) -> list:
    return [{"page": "1"}, {"page":"2"}]
    

@activity.defn
async def get_article(title: str) -> str:
    return {"this": "is", "my" : "article"}
    



