import json

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
from utils.helper_functions import get_custom_logger
from services.langgraph_service.schemas import SearchQuery

log = get_custom_logger(name=__name__)


def get_system_message(message: str) -> SystemMessage:
    return SystemMessage(content=message)


def get_human_message(message: str) -> HumanMessage:
    return HumanMessage(content=message)


def get_graph_configuration(thread_id: str = "1") -> dict:
    return {
        "configurable": {
            "thread_id": thread_id
        }
    }


def convert_messages_to_dicts(messages) -> list[dict]:
    """
    Converts a list of LangChain messages to a list of dictionaries
    with role and content keys.

    Args:
        messages (list): A list of ToolMessage, AIMessage, or HumanMessage objects.

    Returns:
        list: A list of dictionaries with 'role' and 'content'.
    """
    converted_messages = []

    for message in messages:
        if isinstance(message, ToolMessage):
            pass
        elif isinstance(message, AIMessage):
            converted_messages.append({"role": "assistant", "content": message.content, "id": message.id})
        elif isinstance(message, HumanMessage):
            converted_messages.append({"role": "user", "content": message.content, "id": message.id})
        else:
            raise ValueError(f"Unsupported message type: {type(message)}")

    return converted_messages


def convert_dicts_to_messages(dicts):
    """
    Converts a list of dictionaries with 'role' and 'content' to a list of LangChain message objects.

    Args:
        dicts (list): A list of dictionaries with 'role' and 'content'.

    Returns:
        list: A list of ToolMessage, AIMessage, or HumanMessage objects.
    """
    messages = []

    for item in dicts:
        role = item.get("role")
        content = item.get("content")

        if role == "tool":
            messages.append(ToolMessage(content=content))
        elif role == "assistant":
            messages.append(AIMessage(content=content))
        elif role == "user":
            messages.append(HumanMessage(content=content))
        else:
            log.info(f"Skipping role: {role} for item: {item}")

    return messages


async def async_stream(sync_generator):
    for chunk in sync_generator:
        yield chunk


async def streaming_wrapper(agent, messages, graph_config):
    agent.search_graph.update_state(graph_config, {"search_query": SearchQuery(), "search_result": {}})
    async for event in agent.search_graph.astream_events({"messages": messages}, version="v2", config=graph_config):
        if event["event"] == "on_chain_stream":
            if 'messages' in event['data']['chunk']:
                try:
                    if not isinstance(event["data"]["chunk"]["messages"], list):
                        yield event["data"]["chunk"]["messages"].content
                except Exception as e:
                    log.error(e)
                    log.info(f"Content: {event['data']['chunk']['messages']}")

        elif event["event"] == "on_chain_end":
            if event["data"] and "output" in event["data"] and "search_result" in event["data"]["output"]:
                if event["data"]["output"]["search_result"]:
                    yield json.dumps(event["data"]["output"]["search_result"])
                    return
        else:
            try:
                yield ""
            except Exception as e:
                log.error(f"Error occurred in event: event['event'], Error: {str(e)}")
