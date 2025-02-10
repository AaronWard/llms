""" 
The following will allow you to crawl several URLs in parallel.
Useful for when you have a list of URLs you want to grab content for.

1. stream=True: Process results as they become available
2. stream=False: Wait for all results to complete

More advanced info here: https://docs.crawl4ai.com/advanced/multi-url-crawling/
"""
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode

async def quick_parallel_example():
    urls = [
        "https://docs.ag2.ai/docs/use-cases/use-cases/customer-service",
        "https://docs.ag2.ai/docs/use-cases/use-cases/game-design",
        "https://docs.ag2.ai/docs/use-cases/use-cases/travel-planning"
    ]

    run_conf = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        stream=True  # Enable streaming mode
    )

    async with AsyncWebCrawler() as crawler:
        # Stream results as they complete
        async for result in await crawler.arun_many(urls, config=run_conf):
            if result.success:
                print(f"[OK] {result.url}, length: {len(result.markdown_v2.raw_markdown)}")
            else:
                print(f"[ERROR] {result.url} => {result.error_message}")

        # Or get all results at once (default behavior)
        run_conf = run_conf.clone(stream=False)
        results = await crawler.arun_many(urls, config=run_conf)
        for res in results:
            print(res.markdown_v2.raw_markdown)
            if res.success:
                print(f"[OK] {res.url}, length: {len(res.markdown_v2.raw_markdown)}")
            else:
                print(f"[ERROR] {res.url} => {res.error_message}")

if __name__ == "__main__":
    asyncio.run(quick_parallel_example())