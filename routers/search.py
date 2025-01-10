import time

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from services.external_services.oxylabs import get_oxylabs_search_result
from services.langgraph_service.agent import LangGraphAgent
from services.langgraph_service.utils import (
    get_human_message,
    get_graph_configuration,
    streaming_wrapper
)
from utils.helper_functions import get_custom_logger

from config import OXYLABS_PRICING_SOURCE

log = get_custom_logger(name=__name__)

router = APIRouter(tags=["Search"], prefix="/search")
agent = LangGraphAgent(model_name="groq")


@router.post("/generate_search_query")
async def generate_search_query(user_query: str, chat_id: str):
    log.info("Search Query API Call Started.")

    human_message = get_human_message(message=user_query)

    messages = [human_message]

    graph_config = get_graph_configuration(thread_id=chat_id)

    log.info("Calling search agent.")
    return StreamingResponse(streaming_wrapper(agent=agent, messages=messages, graph_config=graph_config))


@router.get("/visualize")
async def visualize():
    log.info(f"Visualizing search graph")
    return agent.visualize()


@router.post("/product_pricing", response_model=dict)
async def product_pricing(product_id: str):
    start_time = time.time()
    log.info(f"Getting product details with product id: {product_id}")

    data = get_oxylabs_search_result(
        search_engine=OXYLABS_PRICING_SOURCE,
        user_query=product_id
    )

    log.info(f"Got product details with product id: {product_id} in {(time.time() - start_time):.2f} seconds.")
    return {
        "pricing_result": data
    }
