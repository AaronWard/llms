""" 
This script demonstrates a simple web crawling example using the Crawl4AI library. It will:
1. Print the first 300 characters of the raw HTML content
2. Print the first 300 characters of the cleaned HTML content
3. print the first 500 characters of the content in Markdown format
4. List all types of media found in the webpage (images, videos, etc.)
5. list any image links found on the page
6. list any internal links found on the page
7. list any external links found on the page


RESULT:
====================
[INIT].... → Crawl4AI 0.4.248
[FETCH]... ↓ https://docs.ag2.ai/docs/contributor-guide/contrib... | Status: True | Time: 0.01s
[COMPLETE] ● https://docs.ag2.ai/docs/contributor-guide/contrib... | Status: True | Total: 0.01s
=== Raw HTML (first 300 chars) ===
<!DOCTYPE html><html lang="en" class="js-focus-visible lg:[--scroll-mt:9.5rem]" style="--font-family-headings-custom: Jersey 10; --font-family-body-custom: Inter;" data-js-focus-visible=""><head><meta charset="utf-8"><meta name="viewport" content="width=device-width"><link rel="apple-touch-icon" typ

=== Cleaned HTML (first 300 chars) ===
<div><main><div><div><div><div><div><div><div><div><a href="/"><span>AG2 home page</span><img alt="light logo" class="w-auto h-7 relative object-contain block dark:hidden" src="https://mintlify.s3.us-west-1.amazonaws.com/ag2ai/logo/ag2.svg"/><img alt="dark logo" class="w-auto h-7 relative object-con
Content (Markdown, first 500 chars):
[AG2 home page![light logo](https://mintlify.s3.us-west-1.amazonaws.com/ag2ai/logo/ag2.svg)![dark logo](https://mintlify.s3.us-west-1.amazonaws.com/ag2ai/logo/ag2-white.svg)](https://docs.ag2.ai/docs/contributor-guide/</>)
Search or ask...
⌘K
Search...
Navigation
Contributor Guide
Contributing to AG2
[Home](https://docs.ag2.ai/docs/contributor-guide/</docs/home/home>)[User Guide](https://docs.ag2.ai/docs/contributor-guide/</docs/user-guide/basic-concepts/installing-ag2>)[API References](https://

---

=== Media Extracted ===
Images:
 - None
Videos:
 - None
Audios:
 - None

No images found.

---

Internal links found:
Internal link: https://docs.ag2.ai/
. . .

No external links found.

"""
import asyncio
from crawl4ai import AsyncWebCrawler
from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig, CacheMode

async def main():
    # Set up browser configuration with verbose logging enabled for debugging
    browser_config = BrowserConfig(verbose=True)
    
    # Define a run configuration with additional crawl options:
    run_config = CrawlerRunConfig(
        # Content filtering options
        word_count_threshold=10,          # Minimum words per content block
        excluded_tags=['form', 'header'], # Exclude specified HTML tags
        exclude_external_links=True,      # Remove external links from the content

        # Content processing options
        process_iframes=True,             # Process content within iframes
        remove_overlay_elements=True,     # Remove overlay elements (popups, modals)

        # Cache control
        cache_mode=CacheMode.ENABLED      # Enable caching if available
    )

    # Initialize and run the asynchronous crawler
    async with AsyncWebCrawler(config=browser_config) as crawler:
        result = await crawler.arun(
            url="https://docs.ag2.ai/docs/contributor-guide/contributing",
            config=run_config
        )

        # Check if the crawl was successful
        if result.success:
            # Print the markdown version of the content (first 500 characters)
            print("=== Raw HTML (first 300 chars) ===")
            print(result.html[:300])
            print("\n=== Cleaned HTML (first 300 chars) ===")
            print(result.cleaned_html[:300])
            print("Content (Markdown, first 500 chars):")
            print(result.markdown[:500])
            print("\n---\n")
            
            
                        # Display extracted media information
            print("=== Media Extracted ===")
            for media_type, items in result.media.items():
                print(f"{media_type.capitalize()}:")
                if items:
                    for item in items:
                        print(f" - {item.get('src', 'N/A')}")
                else:
                    print(" - None")
            print()
            

            # Process and print images if any are found
            images = result.media.get("images", [])
            if images:
                print("Images found:")
                for image in images:
                    print(f"Found image: {image.get('src', 'N/A')}")
            else:
                print("No images found.")

            print("\n---\n")
            
            # Process and print internal links if any are found
            internal_links = result.links.get("internal", [])
            if internal_links:
                print("Internal links found:")
                for link in internal_links:
                    print(f"Internal link: {link.get('href', 'N/A')}")
            else:
                print("No internal links found.")

            # Process and print internal links if any are found
            external_links = result.links.get("external", [])
            if external_links:
                print("External links found:")
                for link in external_links:
                    print(f"External link: {link.get('href', 'N/A')}")
            else:
                print("No external links found.")

        else:
            # Handle errors by printing error details
            print(f"Crawl failed: {result.error_message}")
            print(f"Status code: {result.status_code}")

if __name__ == "__main__":
    asyncio.run(main())
