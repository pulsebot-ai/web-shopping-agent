from pydantic import BaseModel, Field
from typing import List


class SearchQuery(BaseModel):
    search_queries: List[str] = Field(default=[], description="Search queries for retrieval.")
    context: str = Field(default="", description="Context string describing the user intent.")
