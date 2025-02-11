""" 
This script demonstrates the capabilities of the Crawl4AI library by performing two distinct examples:

- **Standard Crawl Example**
  - Crawl Information
  - Raw HTML (first 300 chars)
  - Cleaned HTML (first 300 chars)
  - Markdown Generation Result, which includes:
    - Raw Markdown (first 300 chars)
    - Markdown with Citations
    - References Markdown
    - Fit Markdown (first 300 chars, if available)
    - Fit HTML (first 300 chars, if available)
  - Media Extracted
  - Links Extracted
  - Downloaded Files
  - Screenshot and PDF
  - Additional Fields (extracted content, metadata, error message, session ID, SSL certificate)

- **Structured Extraction Example**
  - Structured Extraction Output

All title headers in the output are printed in ANSI green to enhance readability.
"""
import asyncio
import base64
import json
from crawl4ai import AsyncWebCrawler
from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy

def print_title(title: str):
    # ANSI escape sequence for bright green: \033[92m, reset: \033[0m
    print(f"\033[92m{title}\033[0m")

async def crawl_standard_page():
    """
    Crawl a live page (https://example.com) and demonstrate the various output fields:
      - Raw and cleaned HTML
      - Markdown (detailed MarkdownGenerationResult via markdown_v2)
      - Extracted media and links
      - Screenshot and PDF (if enabled)
      - Response headers, status code, and SSL certificate (if available)
    """
    print_title("=== Standard Crawl Example ===")
    print()

    # Set up a browser configuration (verbose logging enabled)
    browser_config = BrowserConfig(verbose=True)

    # Set up a markdown generator with options
    markdown_generator = DefaultMarkdownGenerator(options={"citations": True, "body_width": 80})

    # Configure the crawl run with various options:
    # - Enable screenshot and PDF capture
    # - Set content filtering options and caching
    # - Include the markdown generator for rich markdown output (returned in markdown_v2)
    run_config = CrawlerRunConfig(
        excluded_tags=['form', 'header', 'footer'],
        process_iframes=True,
        remove_overlay_elements=True,
        cache_mode=CacheMode.ENABLED,
        screenshot=True,
        pdf=True,
        fetch_ssl_certificate=True,  # Assuming this flag is supported
        markdown_generator=markdown_generator
    )

    async with AsyncWebCrawler(config=browser_config) as crawler:
        result = await crawler.arun(url="https://docs.ag2.ai/docs/contributor-guide/contributing", config=run_config)

        # Print general crawl result info
        print_title("Crawl Information")
        print("Crawl URL:", result.url)
        print("Success:", result.success)
        print("Status Code:", result.status_code)
        if result.response_headers:
            print("Response Headers:", result.response_headers)
        print()

        # Display HTML outputs
        print_title("Raw HTML (first 300 chars)")
        print(result.html[:300])
        print()

        print_title("Cleaned HTML (first 300 chars)")
        print(result.cleaned_html[:300] if result.cleaned_html else "None")
        print()

        # Display Markdown outputs (detailed markdown_v2 output)
        print_title("Markdown Generation Result")
        if result.markdown_v2:
            md = result.markdown_v2
            print_title("Raw Markdown (first 300 chars)")
            print(md.raw_markdown[:300])
            print()
            print_title("Markdown with Citations")
            print(md.markdown_with_citations)
            print()
            print_title("References Markdown")
            print(md.references_markdown)
            print()
            if md.fit_markdown:
                print_title("Fit Markdown (first 300 chars)")
                print(md.fit_markdown[:300])
                print()
            if md.fit_html:
                print_title("Fit HTML (first 300 chars)")
                print(md.fit_html[:300])
                print()
        else:
            print("No markdown_v2 output available.")
        print()

        # Display media and links information
        print_title("Media Extracted")
        for media_type, items in result.media.items():
            print(f"{media_type.capitalize()}: {len(items)} item(s)")
            for item in items:
                print(" -", item.get("src", "N/A"))
        print()

        print_title("Links Extracted")
        for link_type, links in result.links.items():
            print(f"{link_type.capitalize()} Links: {len(links)} item(s)")
            for link in links:
                print(" -", link.get("href", "N/A"))
        print()

        # Downloaded files (if any)
        print_title("Downloaded Files")
        if result.downloaded_files:
            print(result.downloaded_files)
        else:
            print("No files downloaded.")
        print()

        # Screenshot (base64 string) and PDF (raw bytes)
        print_title("Screenshot and PDF")
        if result.screenshot:
            print("Screenshot captured")
            screenshot_bytes = base64.b64decode(result.screenshot)
            with open("./output/screenshot.png", "wb") as screenshot_file:
                screenshot_file.write(screenshot_bytes)
        else:
            print("No screenshot available.")
        if result.pdf:
            # Optionally, write PDF bytes to a file
            with open("./output/output.pdf", "wb") as pdf_file:
                pdf_file.write(result.pdf)
            print("PDF captured and saved as 'output.pdf'.")
        else:
            print("No PDF available.")
        print()

        # Additional fields
        print_title("Additional Fields")
        if result.extracted_content:
            print("Extracted Content:")
            print(result.extracted_content)
            print()
        if result.metadata:
            print("Metadata:")
            print(result.metadata)
            print()
        if result.error_message:
            print("Error Message:")
            print(result.error_message)
            print()
        if result.session_id:
            print("Session ID:", result.session_id)
        if result.ssl_certificate:
            print("SSL Certificate Info:", result.ssl_certificate)
        print()
        print_title("=== End of Standard Crawl ===")
        print("\n")

async def structured_extraction_example():
    """
    Demonstrate structured extraction using a CSS-based strategy on raw HTML.
    The structured data is returned in the 'extracted_content' field.
    """
    print_title("=== Structured Extraction Example ===")
    print()

    # Define a simple extraction schema
    schema = {
        "name": "Example Items",
        "baseSelector": "div.item",
        "fields": [
            {"name": "title", "selector": "h2", "type": "text"},
            {"name": "link", "selector": "a", "type": "attribute", "attribute": "href"}
        ]
    }

    # Raw HTML input using the "raw://" protocol (bypassing network requests)
    raw_html = "<div class='item'><h2>Item 1</h2><a href='https://example.com/item1'>Link 1</a></div>"

    # Configure the crawl to use the CSS extraction strategy with no caching
    run_config = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        extraction_strategy=JsonCssExtractionStrategy(schema)
    )

    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url="raw://" + raw_html, config=run_config)

        # The extracted_content should be a JSON string containing our structured data.
        print_title("Structured Extraction Output")
        if result.extracted_content:
            try:
                data = json.loads(result.extracted_content)
                print(json.dumps(data, indent=2))
            except json.JSONDecodeError:
                print("Error decoding extracted content as JSON.")
        else:
            print("No extracted content found.")

    print()
    print_title("=== End of Structured Extraction Example ===")
    print("\n")

async def main():
    await crawl_standard_page()
    await structured_extraction_example()

if __name__ == "__main__":
    asyncio.run(main())
