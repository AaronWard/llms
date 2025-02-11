"""

"""
import asyncio
import json
from crawl4ai import AsyncWebCrawler
from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy

async def crawl_standard_page():
    """
    Crawl a live page (https://example.com) and demonstrate the various output fields:
      - Raw and cleaned HTML
      - Markdown (detailed MarkdownGenerationResult via markdown_v2)
      - Extracted media and links
      - Screenshot and PDF (if enabled)
      - Response headers, status code, and SSL certificate (if available)
    """
    print("=== Standard Crawl Example ===\n")

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
        print("Crawl URL:", result.url)
        print("Success:", result.success)
        print("Status Code:", result.status_code)
        if result.response_headers:
            print("Response Headers:", result.response_headers)
        print()

        # Display HTML outputs
        print("=== Raw HTML (first 300 chars) ===")
        print(result.html[:300])
        print("\n=== Cleaned HTML (first 300 chars) ===")
        print(result.cleaned_html[:300] if result.cleaned_html else "None")
        print()

        # Display Markdown outputs (detailed markdown_v2 output)
        if result.markdown_v2:
            md = result.markdown_v2
            print("=== Markdown Generation Result ===")
            print("Raw Markdown (first 300 chars):")
            print(md.raw_markdown[:300])
            print("\nMarkdown with Citations:")
            print(md.markdown_with_citations)
            print("\nReferences Markdown:")
            print(md.references_markdown)
            if md.fit_markdown:
                print("\nFit Markdown (first 300 chars):")
                print(md.fit_markdown[:300])
            if md.fit_html:
                print("\nFit HTML (first 300 chars):")
                print(md.fit_html[:300])
        else:
            print("No markdown_v2 output available.")
        print()

        # Display media and links information
        print("=== Media Extracted ===")
        for media_type, items in result.media.items():
            print(f"{media_type.capitalize()}: {len(items)} item(s)")
            for item in items:
                print(" -", item.get("src", "N/A"))
        print()

        print("=== Links Extracted ===")
        for link_type, links in result.links.items():
            print(f"{link_type.capitalize()} Links: {len(links)} item(s)")
            for link in links:
                print(" -", link.get("href", "N/A"))
        print()

        # Downloaded files (if any)
        if result.downloaded_files:
            print("Downloaded Files:", result.downloaded_files)
        else:
            print("No files downloaded.")
        print()

        # Screenshot (base64 string) and PDF (raw bytes)
        if result.screenshot:
            print("Screenshot captured (length of base64 string):", len(result.screenshot))
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
        print("\n--- End of Standard Crawl ---\n")


async def structured_extraction_example():
    """
    Demonstrate structured extraction using a CSS-based strategy on raw HTML.
    The structured data is returned in the 'extracted_content' field.
    """
    print("=== Structured Extraction Example ===\n")

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
        if result.extracted_content:
            try:
                data = json.loads(result.extracted_content)
                print("Structured Extraction Output:")
                print(json.dumps(data, indent=2))
            except json.JSONDecodeError:
                print("Error decoding extracted content as JSON.")
        else:
            print("No extracted content found.")

    print("\n--- End of Structured Extraction Example ---\n")


async def main():
    await crawl_standard_page()
    await structured_extraction_example()

if __name__ == "__main__":
    asyncio.run(main())
