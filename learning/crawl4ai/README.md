

```
pip install -U crawl4ai
crawl4ai-setup
crawl4ai-doctor
```

If you encounter any browser-related issues, you can install them manually:
`python -m playwright install --with-deps chromium`



1. Performing a basic crawl to convert a webpage into markdown
2. Example of using configs. Crawl4AI’s crawler can be heavily customized using two main classes:
    1. BrowserConfig: Controls browser behavior 
    2. CrawlerRunConfig: Controls how each crawl runs
3.


**Dispatchers**
- Adaptive: Memory-based dispatchers can pause or slow down based on system resources
- Rate-limiting: Built-in rate limiting with exponential backoff for 429/503 responses
-Real-time Monitoring: Live dashboard of ongoing tasks, memory usage, and performance
- Flexibility: Choose between memory-adaptive or semaphore-based concurrency

----

## TODO:

- Make a web crawler that can implement all of the provided functionalities for, and apply it to https://docs.crawl4ai.com/