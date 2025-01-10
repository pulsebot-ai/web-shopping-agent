import time
import requests

from config import SERPAPI_API_KEY, SERPAPI_SEARCH_URL, SERPAPI_SEARCH_ENGINE
from utils.helper_functions import get_custom_logger

log = get_custom_logger(name=__name__)


def get_serpapi_search_result(user_query: str) -> dict:
    """
    Call SerpApi to get shopping search results
    :param user_query: user search query to be sent to SerpApi for shopping search results
    :return: a json response from SerpApi with search results
    """
    log.info(f"Sending request to SerpApi with search engine: {SERPAPI_SEARCH_ENGINE} and query: {user_query}.")
    start_time = time.time()

    params = {
        "engine": SERPAPI_SEARCH_ENGINE,
        "q": user_query,
        "api_key": SERPAPI_API_KEY
    }

    response = requests.get(SERPAPI_SEARCH_URL, params=params)
    data = response.json()

    if 'error' in data:
        raise Exception(f"SerpApi Error: {data['error']}")

    if 'shopping_results' in data:
        data = data['shopping_results']

    log.info(f"SerpApi response took {(time.time() - start_time):.2f} seconds with search engine: {SERPAPI_SEARCH_ENGINE}.")
    return {"search_result": data}
