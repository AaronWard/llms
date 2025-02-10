"""
Used for for repetitive page structures, where the extraction schema is known and does not require LLM.

RESULT: 
====== 
[INIT].... → Crawl4AI 0.4.248
[FETCH]... ↓ Raw HTML... | Status: True | Time: 0.00s
[SCRAPE].. ◆ Processed Raw HTML... | Time: 2ms
[EXTRACT]. ■ Completed for Raw HTML... | Time: 0.0003519590027281083s
[COMPLETE] ● Raw HTML... | Status: True | Total: 0.00s
[{'title': 'Item 1', 'link': 'https://example.com/item1'}]
"""
import asyncio
import json
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy

async def main():
    schema = {
        "name": "Example Items",
        "baseSelector": "div.item",
        "fields": [
            {"name": "title", "selector": "h2", "type": "text"},
            {"name": "link", "selector": "a", "type": "attribute", "attribute": "href"}
        ]
    }

    raw_html = "<div class='item'><h2>Item 1</h2><a href='https://example.com/item1'>Link 1</a></div>"

    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url="raw://" + raw_html,
            config=CrawlerRunConfig(
                cache_mode=CacheMode.BYPASS,
                extraction_strategy=JsonCssExtractionStrategy(schema)
            )
        )
        # The JSON output is stored in 'extracted_content'
        data = json.loads(result.extracted_content)
        print(data)

if __name__ == "__main__":
    asyncio.run(main())