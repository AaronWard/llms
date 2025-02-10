
""" 
For more complex or irregular pages, a language model 
can parse text intelligently into a structure you define

RESULTS:
===========
Results using local models are not good - local models don't extract all the information
Results using OpenAI models are work perfectly

[
    {
        "project_name": "AutoTx - Crypto Transactions Agent",
        "project_description": "Generates on-chain transactions, which are submitted to a smart account so users can easily approve & execute them.",
        "error": false
    },
    {
        "project_name": "AutoGen Virtual Focus Group",
        "project_description": "A virtual consumer focus group with multiple custom personas, product details, and final analysis created with AutoGen, Ollama/Llama3, and Streamlit.",
        "error": false
    },
    . . .
]
"""
import os
import json
import asyncio
from typing import Dict
from pathlib import Path
from pydantic import BaseModel, Field
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv('../../.env'))
print(os.getenv("OPENAI_API_KEY"))

from crawl4ai import BrowserConfig, CacheMode
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from crawl4ai.extraction_strategy import LLMExtractionStrategy

class TableSchema(BaseModel):
    project_name: str = Field(..., description="Name of the project in the gallery")
    project_description: str = Field(..., description="Project description")

async def extract_structured_data_using_llm(
    provider: str, 
    api_token: str = None, 
    extra_headers: Dict[str, str] = None
):
    print(f"\n--- Extracting Structured Data with {provider} ---")

    if api_token is None and provider != "ollama":
        print(f"API token is required for {provider}. Skipping this example.")
        return

    browser_config = BrowserConfig(headless=True)

    extra_args = {"temperature": 0, "top_p": 0.9, "max_tokens": 4000}
    if extra_headers:
        extra_args["extra_headers"] = extra_headers

    crawler_config = CrawlerRunConfig(
        cache_mode=CacheMode.DISABLED,
        word_count_threshold=1,
        page_timeout=80000,
        extraction_strategy=LLMExtractionStrategy(
            provider=provider,
            api_token=api_token,
            schema=TableSchema.model_json_schema(),
            extraction_type="schema",
            instruction=f"""From the crawled content, extract all mentioned demos in the community gallery.
            along with their descriptions
            Do this for ALL projects listed in the gallery.
            
            FORMAT:
            {json.dumps(TableSchema.model_json_schema(), indent=2)}
            """,
            extra_args=extra_args,
        ),
    )

    async with AsyncWebCrawler(config=browser_config) as crawler:
        result = await crawler.arun(
            url="https://docs.ag2.ai/docs/use-cases/community-gallery/community-gallery", config=crawler_config
        )
        print(result.extracted_content)

if __name__ == "__main__":
    # asyncio.run(
    #     extract_structured_data_using_llm(
    #         # provider="ollama/hf.co/bartowski/Qwen2.5-7B-Instruct-1M-GGUF:F16", 
    #         provider="ollama/deepseek-r1:14b", 
    #         api_token="no-token"
    #     )
    # )

    asyncio.run(
        extract_structured_data_using_llm(
            provider="openai/gpt-4o-mini", api_token=os.getenv("OPENAI_API_KEY")
        )
    )