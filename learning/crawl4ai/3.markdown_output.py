""" 
Supposedly DefaultMarkdownGenerator is used for generating citations from links in markdown.
Documentation is shit, doesn't even explain what fit_markdown is used. 
"""
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from crawl4ai.content_filter_strategy import PruningContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
from crawl4ai import BrowserConfig, CacheMode

async def main():
    async with AsyncWebCrawler() as crawler:
        
        md_generator = DefaultMarkdownGenerator(
        content_filter=PruningContentFilter(threshold=0.4, threshold_type="fixed")
        )

        config = CrawlerRunConfig(
            cache_mode=CacheMode.BYPASS,
            markdown_generator=md_generator
        )

        
        result = await crawler.arun("https://meaningness.com/geeks-mops-sociopaths", config=config)
        print("Raw Markdown length:", len(result.markdown_v2.raw_markdown))
        print("Fit Markdown length:", len(result.markdown_v2.fit_markdown))
        print("Result", result.markdown_v2.raw_markdown)

        
if __name__ == "__main__":
    asyncio.run(main())