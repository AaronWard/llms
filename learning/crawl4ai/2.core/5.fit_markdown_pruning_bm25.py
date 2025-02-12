""" 
PruningContentFilter and BM25ContentFilter are two content filters that can be used to

RESULTS:
==========
Despite testing with many different parameter combinations, the PruningContentFilter and BM25ContentFilter
don't seem to produce different results for the given URL. This could be due to the nature of the content. 

"""
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from crawl4ai.content_filter_strategy import PruningContentFilter, BM25ContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

# Target URL for testing.
URL = "https://docs.ag2.ai/docs/blog/2023-06-28-MathChat/index"

def print_title(title: str):
    """Prints the given title in bright ANSI green for clear separation."""
    print(f"\033[92m{title}\033[0m")

async def test_pruning_parameters():
    """
    Tests several parameter combinations for PruningContentFilter and compares results.
    
    For each parameter set, the crawler generates:
      - raw_markdown (full conversion)
      - fit_markdown (filtered output)
    
    It then prints:
      - The lengths of raw and fit markdown.
      - A snippet of the fit markdown (or a fallback snippet from the raw markdown if fit_markdown is empty).
    
    If all tests produce an empty fit_markdown, it means the filter’s heuristics determine that
    none of the content blocks meet the criteria for being “dense” or “relevant” on this page.
    """
    print_title("Testing Various PruningContentFilter Parameters")
    
    # List of parameter sets to test.
    pruning_params_list = [
        {"threshold": 0.1, "min_word_threshold": 2},
        {"threshold": 0.5, "min_word_threshold": 22},
        {"threshold": 0.9, "min_word_threshold": 55},
    ]
    
    for params in pruning_params_list:
        print_title(f"Pruning Params: threshold={params['threshold']}, min_word_threshold={params['min_word_threshold']}")
        
        # Create the pruning filter with current parameters.
        prune_filter = PruningContentFilter(
            threshold=params["threshold"],
            threshold_type="fixed",  # Uses dynamic threshold based on content characteristics. # fixed
            min_word_threshold=params["min_word_threshold"]
        )
        
        # Create a markdown generator that uses the pruning filter.
        md_generator = DefaultMarkdownGenerator(content_filter=prune_filter)
        
        # Configure the crawler run.
        config = CrawlerRunConfig(
            markdown_generator=md_generator
        )
        
        async with AsyncWebCrawler() as crawler:
            result = await crawler.arun(url=URL, config=config)
            if result.success:
                raw_len = len(result.markdown_v2.raw_markdown)
                fit_len = len(result.markdown_v2.fit_markdown)
                print("Raw Markdown length:", raw_len)
                print("Fit Markdown length:", fit_len)
                if fit_len == 0:
                    print("No filtered content produced. Showing raw snippet:")
                    print(result.markdown_v2.raw_markdown[:300])
                else:
                    print("Snippet of Fit Markdown:")
                    print(result.markdown_v2.fit_markdown[:300])
            else:
                print("Error during crawl with PruningContentFilter:", result.error_message)
        print("-" * 80)

async def test_bm25_parameters():
    """
    Tests several parameter combinations for BM25ContentFilter and compares results.
    
    For each parameter set, the crawler generates:
      - raw_markdown (full conversion)
      - fit_markdown (filtered output based on query relevance)
    
    It then prints:
      - The lengths of raw and fit markdown.
      - A snippet of the filtered output (or a fallback snippet from raw markdown if empty).
    
    If the filtered output is empty for all settings, then the BM25 algorithm deems no text blocks as
    sufficiently relevant for the provided query on this page.
    """
    print_title("Testing Various BM25ContentFilter Parameters")
    
    # List of parameter sets to test.
    bm25_params_list = [
        {"user_query": "apache", "bm25_threshold": 0.01},
        {"user_query": "apache", "bm25_threshold": 0.5},
        {"user_query": "apache", "bm25_threshold": 0.9},
    ]
    
    for params in bm25_params_list:
        print_title(f"BM25 Params: user_query='{params['user_query']}', bm25_threshold={params['bm25_threshold']}")
        
        # Create the BM25 filter with current parameters.
        bm25_filter = BM25ContentFilter(
            user_query=params["user_query"],
            bm25_threshold=params["bm25_threshold"]
        )
        
        # Create a markdown generator that uses the BM25 filter.
        md_generator = DefaultMarkdownGenerator(content_filter=bm25_filter)
        
        # Configure the crawler run.
        config = CrawlerRunConfig(
            markdown_generator=md_generator
        )
        
        async with AsyncWebCrawler() as crawler:
            result = await crawler.arun(url=URL, config=config)
            if result.success:
                raw_len = len(result.markdown_v2.raw_markdown)
                fit_len = len(result.markdown_v2.fit_markdown)
                print("Raw Markdown length:", raw_len)
                print("Fit Markdown length:", fit_len)
                if fit_len == 0:
                    print("No filtered content produced. Showing raw snippet:")
                    print(result.markdown_v2.raw_markdown[:300])
                else:
                    print("Snippet of Fit Markdown:")
                    print(result.markdown_v2.fit_markdown[:300])
            else:
                print("Error during crawl with BM25ContentFilter:", result.error_message)
        print("-" * 80)

async def main():
    await test_pruning_parameters()
    await test_bm25_parameters()

if __name__ == "__main__":
    asyncio.run(main())
