"""


1. BrowserConfig: Controls browser behavior (headless or full UI, user agent, JavaScript toggles, etc.).
2. CrawlerRunConfig: Controls how each crawl runs (caching, extraction, timeouts, hooking, etc.).
"""

import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode

async def main():
    browser_conf = BrowserConfig(headless=True)  # or False to see the browser
    run_conf = CrawlerRunConfig(
        cache_mode=CacheMode.ENABLED # BYPASS, DISABLED, ENABLED (default), READ_ONLY, WRITE_ONLY
    )

    async with AsyncWebCrawler(config=browser_conf) as crawler:
        result = await crawler.arun(
            url="https://meaningness.com/geeks-mops-sociopaths",
            config=run_conf
        )
        print(result.markdown)

if __name__ == "__main__":
    asyncio.run(main())