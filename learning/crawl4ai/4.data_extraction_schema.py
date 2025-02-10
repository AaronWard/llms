""" 
> utility to automatically generate extraction schemas using LLM. 
> This is a one-time cost that gives you a reusable schema for fast, LLM-free extractions:

DOES NOT WORK, Litellm is a piece of shit
"""
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy
import litellm

litellm.set_verbose=True

# Generate a schema (one-time cost)
html = "<div class='product'><h2>Gaming Laptop</h2><span class='price'>$999.99</span></div>"

# Using OpenAI (requires API token)
# schema = JsonCssExtractionStrategy.generate_schema(
#     html,
#     llm_provider="openai/gpt-4o",  # Default provider
#     api_token="your-openai-token"  # Required for OpenAI
# )

# Or using Ollama (open source, no token needed)
schema = JsonCssExtractionStrategy.generate_schema(
    html,
    provider="ollama/llama3.1:latest",  # Open source alternative
    api_token=None  # Not needed for Ollama
)

# Use the schema for fast, repeated extractions
strategy = JsonCssExtractionStrategy(schema)