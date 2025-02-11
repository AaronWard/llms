"""
Browser & Crawler Configuration Demo (Updated)
-----------------------------------------------
This script demonstrates the key capabilities of Crawl4AI’s configuration classes with updated rate limiting.
It covers:

- **BrowserConfig Essentials**
  - browser_type, headless, proxy_config, viewport settings, verbose, etc.

- **CrawlerRunConfig Essentials**
  - word_count_threshold, extraction_strategy, markdown_generator, cache_mode, js_code, wait_for, screenshot, pdf.
  - New rate limiting parameters:
      - semaphore_count: maximum concurrent crawl sessions.
      - mean_delay: average delay between requests.
      - max_range: maximum delay range.

- **Helper Methods**
  - clone() to create modified copies of configurations.

- **Minimal Example**
  - Executes a crawl and saves screenshot/PDF outputs in ./output.
"""

import asyncio
import json
import base64
import os

# Import configuration classes from async_configs
from crawl4ai import AsyncWebCrawler
# from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai import BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy

def print_title(title: str):
    """Prints the given title in bright ANSI green."""
    print(f"\033[92m{title}\033[0m")

async def main():
    # Create the output directory for screenshots and PDFs.
    os.makedirs("./output2", exist_ok=True)
    
    # -------------------------------
    # 1. BrowserConfig Examples
    # -------------------------------
    print_title("BrowserConfig Examples")
    
    # Base BrowserConfig: using chromium in headless mode, with text mode enabled.
    base_browser = BrowserConfig(
        browser_type="chromium",   # Options: "chromium", "firefox", or "webkit"
        headless=True,             # True for headless mode (invisible browser)
        text_mode=True,            # Disable images for faster, text-only crawling
        viewport_width=1280,       # Browser window width (in pixels)
        viewport_height=720,       # Browser window height (in pixels)
        verbose=True               # Enable verbose logging for debugging
    )
    
    # Clone to create a debug browser configuration (visible browser for debugging).
    debug_browser = base_browser.clone(
        headless=False,            # Set headless to False to see the browser UI
        verbose=True               # Keep verbose logging enabled
    )
    
    print("Base BrowserConfig:", base_browser.__dict__)
    print("Debug BrowserConfig:", debug_browser.__dict__)
    print()

    # -------------------------------
    # 2. CrawlerRunConfig Examples
    # -------------------------------
    print_title("CrawlerRunConfig Examples")
    
    # JavaScript snippet to simulate clicking a "Load More" button.
    js_code_snippet = "document.querySelector('button#loadMore')?.click()"  # Click "Load More" if present
    
    # Define an extraction strategy using CSS selectors.
    schema = {
        "name": "Articles",              # Name of the extraction schema
        "baseSelector": "div.article",   # Base CSS selector for articles
        "fields": [
            {"name": "title", "selector": "h2", "type": "text"},  # Extract text from <h2> as title
            {"name": "link", "selector": "a", "type": "attribute", "attribute": "href"}  # Extract href attribute from <a>
        ]
    }
    extraction = JsonCssExtractionStrategy(schema)
    
    # Base CrawlerRunConfig with caching enabled and extraction strategy set.
    base_config = CrawlerRunConfig(
        word_count_threshold=200,           # Minimum word count before a block is considered valid
        cache_mode=CacheMode.ENABLED,       # Use caching (ENABLED, BYPASS, or DISABLED)
        extraction_strategy=extraction,     # Apply the CSS extraction strategy defined above
        wait_for="networkidle",             # Wait until network activity is idle before extracting content, means that the page has finished fetching all necessary resources 
        screenshot=True,                    # Capture a screenshot of the page
        pdf=True                            # Capture a PDF of the page
    )
    
    # Clone to create a streaming variant with updated rate limiting parameters.
    stream_config = base_config.clone(
        stream=True,                      # Enable streaming mode (process results as they arrive)
        cache_mode=CacheMode.BYPASS,      # Bypass cache to force a fresh crawl
        semaphore_count=3,                # Maximum concurrent crawl sessions allowed
        mean_delay=2.0,                   # Average delay (in seconds) between requests
        max_range=60.0                    # Maximum delay range (in seconds) if needed
    )
    
    # Clone to create a debug configuration variant with JS code and a specific wait condition.
    debug_config = base_config.clone(
        js_code=js_code_snippet,          # JavaScript to execute on the page (simulate user interaction)
        wait_for="css:h1",                # Wait for an element with class .loaded-content before extracting, It minimizes the risk of extracting incomplete or
                                          # incorrect data due to the page not being fully loaded when the extraction occurs.
        verbose=True                      # Enable verbose logging for this crawl run
    )
    
    print("Base CrawlerRunConfig:", base_config.__dict__)
    print("Stream CrawlerRunConfig:", stream_config.__dict__)
    print("Debug CrawlerRunConfig:", debug_config.__dict__)
    print()

    # -------------------------------
    # 3. Putting It All Together: Execute a Crawl
    # -------------------------------
    print_title("Executing Crawl with Configs")
    
    # Use the debug browser configuration and debug run configuration for demonstration.
    async with AsyncWebCrawler(config=debug_browser) as crawler:
        # Crawl a test page (replace with a valid URL as needed).
        url = "https://example.com"
        result = await crawler.arun(url=url, config=debug_config)
        
        if result.success:
            # Output extracted content or markdown snippet.
            if result.extracted_content:
                print_title("Extracted Content")
                print(result.extracted_content)
            elif result.markdown:
                print_title("Markdown Output")
                print(result.markdown[:300])
            else:
                print("No extracted content or markdown available.")
            
            # Save the screenshot (if available) as PNG in the ./output directory.
            if result.screenshot:
                screenshot_bytes = base64.b64decode(result.screenshot)
                screenshot_path = "./output/screenshot2.png"
                with open(screenshot_path, "wb") as f:
                    f.write(screenshot_bytes)
                print_title("Screenshot Saved")
                print(f"Screenshot saved to {screenshot_path}")
            
            # Save the PDF (if available) in the ./output directory.
            if result.pdf:
                pdf_path = "./output/page2.pdf"
                with open(pdf_path, "wb") as f:
                    f.write(result.pdf)
                print_title("PDF Saved")
                print(f"PDF saved to {pdf_path}")
        else:
            print("Error during crawl:", result.error_message)
        
        print()
        print_title("Crawl Completed")
    
if __name__ == "__main__":
    asyncio.run(main())



""" 
(default) aw@aw 2.core % python 3.browser_crawler_config.py
BrowserConfig Examples
Base BrowserConfig: {'browser_type': 'chromium', 'headless': True, 'use_managed_browser': False, 'cdp_url': None, 'use_persistent_context': False, 'user_data_dir': None, 'chrome_channel': 'chromium', 'channel': 'chromium', 'proxy': None, 'proxy_config': None, 'viewport_width': 1280, 'viewport_height': 720, 'accept_downloads': False, 'downloads_path': None, 'storage_state': None, 'ignore_https_errors': True, 'java_script_enabled': True, 'cookies': [], 'headers': {'sec-ch-ua': '"Chromium";v="116", "Not_A Brand";v="8", "Google Chrome";v="116"'}, 'user_agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/116.0.0.0 Safari/537.36', 'user_agent_mode': '', 'user_agent_generator_config': {}, 'text_mode': True, 'light_mode': False, 'extra_args': [], 'sleep_on_close': False, 'verbose': True, 'debugging_port': 9222, 'browser_hint': '"Chromium";v="116", "Not_A Brand";v="8", "Google Chrome";v="116"'}
Debug BrowserConfig: {'browser_type': 'chromium', 'headless': False, 'use_managed_browser': False, 'cdp_url': None, 'use_persistent_context': False, 'user_data_dir': None, 'chrome_channel': 'chromium', 'channel': 'chromium', 'proxy': None, 'proxy_config': None, 'viewport_width': 1280, 'viewport_height': 720, 'accept_downloads': False, 'downloads_path': None, 'storage_state': None, 'ignore_https_errors': True, 'java_script_enabled': True, 'cookies': [], 'headers': {'sec-ch-ua': '"Chromium";v="116", "Not_A Brand";v="8", "Google Chrome";v="116"'}, 'user_agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/116.0.0.0 Safari/537.36', 'user_agent_mode': '', 'user_agent_generator_config': {}, 'text_mode': True, 'light_mode': False, 'extra_args': [], 'sleep_on_close': False, 'verbose': True, 'debugging_port': 9222, 'browser_hint': '"Chromium";v="116", "Not_A Brand";v="8", "Google Chrome";v="116"'}

CrawlerRunConfig Examples
Base CrawlerRunConfig: {'url': None, 'word_count_threshold': 200, 'extraction_strategy': <crawl4ai.extraction_strategy.JsonCssExtractionStrategy object at 0x10683b710>, 'chunking_strategy': <crawl4ai.chunking_strategy.RegexChunking object at 0x107d2fc50>, 'markdown_generator': None, 'content_filter': None, 'only_text': False, 'css_selector': None, 'excluded_tags': [], 'excluded_selector': '', 'keep_data_attributes': False, 'remove_forms': False, 'prettiify': False, 'parser_type': 'lxml', 'scraping_strategy': <crawl4ai.content_scraping_strategy.WebScrapingStrategy object at 0x10532c5d0>, 'proxy_config': None, 'fetch_ssl_certificate': False, 'cache_mode': <CacheMode.ENABLED: 'enabled'>, 'session_id': None, 'bypass_cache': False, 'disable_cache': False, 'no_cache_read': False, 'no_cache_write': False, 'shared_data': None, 'wait_until': 'domcontentloaded', 'page_timeout': 60000, 'wait_for': 'networkidle', 'wait_for_images': False, 'delay_before_return_html': 0.1, 'mean_delay': 0.1, 'max_range': 0.3, 'semaphore_count': 5, 'js_code': None, 'js_only': False, 'ignore_body_visibility': True, 'scan_full_page': False, 'scroll_delay': 0.2, 'process_iframes': False, 'remove_overlay_elements': False, 'simulate_user': False, 'override_navigator': False, 'magic': False, 'adjust_viewport_to_content': False, 'screenshot': True, 'screenshot_wait_for': None, 'screenshot_height_threshold': 10000, 'pdf': True, 'image_description_min_word_threshold': 1, 'image_score_threshold': 2, 'exclude_external_images': False, 'exclude_social_media_domains': ['facebook.com', 'twitter.com', 'x.com', 'linkedin.com', 'instagram.com', 'pinterest.com', 'tiktok.com', 'snapchat.com', 'reddit.com'], 'exclude_external_links': False, 'exclude_social_media_links': False, 'exclude_domains': [], 'verbose': True, 'log_console': False, 'stream': False, 'check_robots_txt': False, 'user_agent': None, 'user_agent_mode': None, 'user_agent_generator_config': {}}
Stream CrawlerRunConfig: {'url': None, 'word_count_threshold': 200, 'extraction_strategy': <crawl4ai.extraction_strategy.JsonCssExtractionStrategy object at 0x10683b710>, 'chunking_strategy': <crawl4ai.chunking_strategy.RegexChunking object at 0x107d2fc50>, 'markdown_generator': None, 'content_filter': None, 'only_text': False, 'css_selector': None, 'excluded_tags': [], 'excluded_selector': '', 'keep_data_attributes': False, 'remove_forms': False, 'prettiify': False, 'parser_type': 'lxml', 'scraping_strategy': <crawl4ai.content_scraping_strategy.WebScrapingStrategy object at 0x10532c5d0>, 'proxy_config': None, 'fetch_ssl_certificate': False, 'cache_mode': <CacheMode.BYPASS: 'bypass'>, 'session_id': None, 'bypass_cache': False, 'disable_cache': False, 'no_cache_read': False, 'no_cache_write': False, 'shared_data': None, 'wait_until': 'domcontentloaded', 'page_timeout': 60000, 'wait_for': 'networkidle', 'wait_for_images': False, 'delay_before_return_html': 0.1, 'mean_delay': 2.0, 'max_range': 60.0, 'semaphore_count': 3, 'js_code': None, 'js_only': False, 'ignore_body_visibility': True, 'scan_full_page': False, 'scroll_delay': 0.2, 'process_iframes': False, 'remove_overlay_elements': False, 'simulate_user': False, 'override_navigator': False, 'magic': False, 'adjust_viewport_to_content': False, 'screenshot': True, 'screenshot_wait_for': None, 'screenshot_height_threshold': 10000, 'pdf': True, 'image_description_min_word_threshold': 1, 'image_score_threshold': 2, 'exclude_external_images': False, 'exclude_social_media_domains': ['facebook.com', 'twitter.com', 'x.com', 'linkedin.com', 'instagram.com', 'pinterest.com', 'tiktok.com', 'snapchat.com', 'reddit.com'], 'exclude_external_links': False, 'exclude_social_media_links': False, 'exclude_domains': [], 'verbose': True, 'log_console': False, 'stream': True, 'check_robots_txt': False, 'user_agent': None, 'user_agent_mode': None, 'user_agent_generator_config': {}}
Debug CrawlerRunConfig: {'url': None, 'word_count_threshold': 200, 'extraction_strategy': <crawl4ai.extraction_strategy.JsonCssExtractionStrategy object at 0x10683b710>, 'chunking_strategy': <crawl4ai.chunking_strategy.RegexChunking object at 0x107d2fc50>, 'markdown_generator': None, 'content_filter': None, 'only_text': False, 'css_selector': None, 'excluded_tags': [], 'excluded_selector': '', 'keep_data_attributes': False, 'remove_forms': False, 'prettiify': False, 'parser_type': 'lxml', 'scraping_strategy': <crawl4ai.content_scraping_strategy.WebScrapingStrategy object at 0x10532c5d0>, 'proxy_config': None, 'fetch_ssl_certificate': False, 'cache_mode': <CacheMode.ENABLED: 'enabled'>, 'session_id': None, 'bypass_cache': False, 'disable_cache': False, 'no_cache_read': False, 'no_cache_write': False, 'shared_data': None, 'wait_until': 'domcontentloaded', 'page_timeout': 60000, 'wait_for': 'css:.loaded-content', 'wait_for_images': False, 'delay_before_return_html': 0.1, 'mean_delay': 0.1, 'max_range': 0.3, 'semaphore_count': 5, 'js_code': "document.querySelector('button#loadMore')?.click()", 'js_only': False, 'ignore_body_visibility': True, 'scan_full_page': False, 'scroll_delay': 0.2, 'process_iframes': False, 'remove_overlay_elements': False, 'simulate_user': False, 'override_navigator': False, 'magic': False, 'adjust_viewport_to_content': False, 'screenshot': True, 'screenshot_wait_for': None, 'screenshot_height_threshold': 10000, 'pdf': True, 'image_description_min_word_threshold': 1, 'image_score_threshold': 2, 'exclude_external_images': False, 'exclude_social_media_domains': ['facebook.com', 'twitter.com', 'x.com', 'linkedin.com', 'instagram.com', 'pinterest.com', 'tiktok.com', 'snapchat.com', 'reddit.com'], 'exclude_external_links': False, 'exclude_social_media_links': False, 'exclude_domains': [], 'verbose': True, 'log_console': False, 'stream': False, 'check_robots_txt': False, 'user_agent': None, 'user_agent_mode': None, 'user_agent_generator_config': {}}
"""