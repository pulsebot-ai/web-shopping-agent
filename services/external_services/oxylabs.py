import time

import requests

from utils.helper_functions import get_custom_logger
from config import OXYLABS_SEARCH_URL, OXYLABS_USERNAME, OXYLABS_USER_PASSWORD, OXYLABS_SEARCH_SOURCE

log = get_custom_logger(name=__name__)


def get_oxylabs_search_result(search_engine: str, user_query: str, geo_location: str = 'United States') -> dict:
    log.info(f"Sending request to Oxylabs with search engine: {search_engine} and query: {user_query}.")
    start_time = time.time()
    payload = {
        'source': search_engine,
        'domain': 'com',
        'query': user_query,
        'parse': 'true',
        'geo_location': geo_location,
        'pages': 1,
    }

    response = requests.post(OXYLABS_SEARCH_URL, json=payload, auth=(OXYLABS_USERNAME, OXYLABS_USER_PASSWORD))
    data = response.json()
    if 'results' in data:
        data = data['results'][0]['content']

        if search_engine == OXYLABS_SEARCH_SOURCE:
            data = {"products": data['results']['organic']}

    log.info(f"Oxylabs response took {(time.time() - start_time):.2f} seconds with search engine: {search_engine}.")
    return data
