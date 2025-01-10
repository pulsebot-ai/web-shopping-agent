import os
from dotenv import load_dotenv

load_dotenv()

LLM_CONFIG_GROQ = os.getenv("LLM_CONFIG_GROQ", "llama-3.1,YOUR_API_KEY")
LLM_CONFIG_OLLAMA = os.getenv("LLM_CONFIG_OLLAMA", "llama3.1")
LLM_CONFIG_OPENAI = os.getenv("LLM_CONFIG_OPENAI", "YOUR_MODEL,YOUR_API_KEY")

SERPAPI_SEARCH_URL = os.getenv("SERPAPI_SEARCH_URL", "https://serpapi.com/search")
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY", "YOUR_API_KEY")
SERPAPI_SEARCH_ENGINE = os.getenv("SERPAPI_SEARCH_ENGINE", "google_shopping")

OXYLABS_SEARCH_URL = os.getenv("OXYLABS_SEARCH_URL", "https://realtime.oxylabs.io/v1/queries")
OXYLABS_USERNAME = os.getenv("OXYLABS_USERNAME", "YOUR_USERNAME")
OXYLABS_USER_PASSWORD = os.getenv("OXYLABS_USER_PASSWORD", "YOUR_PASSWORD")
OXYLABS_SEARCH_SOURCE = os.getenv("OXYLABS_SEARCH_SOURCE", "google_shopping_search")
OXYLABS_PRICING_SOURCE = os.getenv("OXYLABS_PRICING_SOURCE", "google_shopping_pricing")

DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root@localhost/your_db_name")
