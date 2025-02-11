""" 


Raw Markdown Generation: 
The raw markdown is simply the HTML of the page converted into markdown. 
It keeps everything—main content, navigation menus, footers, and even some extra formatting that might not be useful.

Filtered Markdown Generation (fit_markdown):
Filtered markdown takes the raw markdown and then uses a content filter (like a PruningContentFilter) to remove the extra noise
(e.g., headers, footers, navigation links, ads). The result is a cleaner version that focuses only on the main, important content.

"""
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
from crawl4ai.content_filter_strategy import PruningContentFilter

def print_title(title: str):
    """Prints the given title in bright ANSI green for clear separation."""
    print(f"\033[92m{title}\033[0m")

async def basic_markdown_generation():
    """
    Demonstrates generating markdown from a web page using DefaultMarkdownGenerator 
    without any additional filtering.
    
    What it does:
    - Configures CrawlerRunConfig with DefaultMarkdownGenerator.
    - Crawls "https://example.com".
    - Prints the raw markdown output.
    """
    print_title("Basic Markdown Generation Example")
    
    # Configure run settings to generate markdown from the page HTML.
    config = CrawlerRunConfig(
        markdown_generator=DefaultMarkdownGenerator()  # Use default HTML-to-markdown conversion.
    )
    
    # Start the asynchronous crawler.
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun("https://example.com", config=config)
        if result.success:
            print_title("Raw Markdown Output")
            print(result.markdown)  # Print the unfiltered markdown.
        else:
            print("Crawl failed:", result.error_message)
    print()  # Blank line for separation.

async def filtered_markdown_generation():
    """
    Demonstrates generating markdown with a content filter applied.
    
    What it does:
    - Sets up a PruningContentFilter to remove extraneous content (noise, boilerplate).
    - Configures DefaultMarkdownGenerator with the content filter and custom options.
    - Crawls a sample page and prints both the raw markdown and the filtered markdown.
    
    Note:
    The original example used "https://news.example.com/tech" as a placeholder, 
    but that domain is not resolvable. For this demonstration, we use "https://example.com".
    """
    print_title("Filtered Markdown Generation Example (Using PruningContentFilter)")
    
    # Create a pruning filter to remove noise:
    prune_filter = PruningContentFilter(
        threshold=0.6,            # Blocks scoring below this threshold are removed.
        threshold_type="fixed",   # Use fixed threshold comparison.
        min_word_threshold=50     # Discard blocks with fewer than 50 words.
    )
    
    # Configure the markdown generator with the content filter and additional options:
    md_generator = DefaultMarkdownGenerator(
        content_filter=prune_filter,  # Apply the pruning filter.
        options={
            "ignore_links": True,    # Remove hyperlinks from the markdown.
            "body_width": 80         # Wrap text at 80 characters.
        }
    )
    
    # For demonstration, we use "https://example.com" instead of a non-resolvable URL.
    url_for_filtered = "https://example.com"
    
    # Configure the crawler run with the markdown generator.
    config = CrawlerRunConfig(
        markdown_generator=md_generator
    )
    
    # Start the asynchronous crawler.
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url_for_filtered, config=config)
        if result.success:
            print_title("Raw Markdown Output")
            print(result.markdown)  # The full unfiltered markdown conversion.
            
            # If a content filter is applied, we also get a filtered ("fit") version.
            # Depending on your version, this might be available as result.markdown_v2.
            md_obj = result.markdown_v2  # MarkdownGenerationResult object with detailed fields.
            print_title("Filtered Markdown Output (fit_markdown)")
            print(md_obj.fit_markdown)  # The pruned version focusing on the main content.
        else:
            print("Crawl failed:", result.error_message)
    print()  # Blank line for separation.

async def main():
    # Run both examples sequentially.
    await basic_markdown_generation()
    await filtered_markdown_generation()

if __name__ == "__main__":
    asyncio.run(main())
