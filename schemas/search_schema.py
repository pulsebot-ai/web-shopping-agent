from pydantic import BaseModel, Field


class GenerateSearchQueryOutput(BaseModel):
    user_query: str = Field(default="", description="User query for retrieval.")
    search_query: str = Field(default="", description="Search query for retrieval if user query is related to search.")
    llm_response: str = Field(default="", description="LLM response if there's no search query.")
    search_result: dict = Field(default={}, description="Search results against query if user query is search related.")
