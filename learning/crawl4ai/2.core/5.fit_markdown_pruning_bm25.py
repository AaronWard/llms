import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from crawl4ai.content_filter_strategy import PruningContentFilter, BM25ContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

def print_title(title: str):
    """Prints the given title in bright ANSI green for clear separation."""
    print(f"\033[92m{title}\033[0m")

async def fit_markdown_with_pruning():
    """
    Demonstrates fit markdown generation using PruningContentFilter.
    
    This filter discards low-value text blocks based on factors such as text density,
    link density, and word count. The output is a pruned version of the full markdown,
    focusing on the most 'dense' or important text.
    
    Steps:
    1. Create a PruningContentFilter with a dynamic threshold and minimum word threshold.
    2. Insert this filter into a DefaultMarkdownGenerator.
    3. Pass the generator to CrawlerRunConfig.
    4. Crawl a target website and print both the raw and pruned markdown lengths.
    """
    print_title("Fit Markdown with PruningContentFilter")
    
    # Step 1: Create a pruning filter.
    prune_filter = PruningContentFilter(
        threshold=0.1,           # Lower values retain more content; higher values prune more aggressively.
        threshold_type="dynamic", # "dynamic" allows the threshold to adjust based on content characteristics.
        min_word_threshold=2      # Ignore content blocks with fewer than 5 words.
    )
    
    # Step 2: Create a markdown generator that uses the pruning filter.
    md_generator = DefaultMarkdownGenerator(content_filter=prune_filter)
    
    # Step 3: Configure the crawler run to use this markdown generator.
    config = CrawlerRunConfig(
        markdown_generator=md_generator
    )
    
    # Step 4: Crawl a target website (here, Hacker News for demonstration).
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url="https://news.ycombinator.com", config=config)
        if result.success:
            # Print the lengths of raw markdown versus the pruned ("fit") markdown.
            print("Raw Markdown length:", len(result.markdown_v2.raw_markdown))
            print("Fit Markdown length:", len(result.markdown_v2.fit_markdown))
        else:
            print("Error during crawl with PruningContentFilter:", result.error_message)
    print()  # Blank line for separation.

async def fit_markdown_with_bm25():
    """
    Demonstrates fit markdown generation using BM25ContentFilter.
    
    BM25ContentFilter uses a classical text ranking algorithm to keep only the text
    blocks that are highly relevant to a specific query (e.g., "startup fundraising tips").
    This results in a filtered markdown that emphasizes the content most relevant to that query.
    
    Steps:
    1. Create a BM25ContentFilter with a specific user query and threshold.
    2. Insert this filter into a DefaultMarkdownGenerator.
    3. Pass the generator to CrawlerRunConfig.
    4. Crawl a target website and print the filtered markdown output.
    """
    print_title("Fit Markdown with BM25ContentFilter")
    
    # Step 1: Create a BM25 filter with a target query.
    bm25_filter = BM25ContentFilter(
        user_query="Markdown",  # Focus on content relevant to this query.
        bm25_threshold=0.1  # Higher thresholds return fewer, more relevant text blocks.
    )
    
    # Step 2: Create a markdown generator that uses the BM25 filter.
    md_generator = DefaultMarkdownGenerator(content_filter=bm25_filter)
    
    # Step 3: Configure the crawler run to use this markdown generator.
    config = CrawlerRunConfig(
        markdown_generator=md_generator
    )
    
    # Step 4: Crawl the target website (using Hacker News as an example).
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url="https://news.ycombinator.com", config=config)
        if result.success:
            # Print the filtered ("fit") markdown that highlights content relevant to the query.
            print("Fit Markdown (BM25 query-based):")
            print(result.markdown_v2.fit_markdown)
        else:
            print("Error during crawl with BM25ContentFilter:", result.error_message)
    print()  # Blank line for separation.

async def main():
    # Run both filtering examples sequentially.
    await fit_markdown_with_pruning()
    await fit_markdown_with_bm25()

if __name__ == "__main__":
    asyncio.run(main())
