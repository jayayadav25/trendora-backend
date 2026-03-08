from typing import List, Dict
from pydantic import BaseModel

class SearchItem(BaseModel):
    product_id: int
    title: str
    gender: str
    final_score: float

class SearchResponse(BaseModel):
    query: str
    total_results: int
    items: List[SearchItem]
    facets: Dict