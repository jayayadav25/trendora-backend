from fastapi import APIRouter, Query
from online_serving.services.search_pipeline import SearchPipeline
from online_serving.schemas.search_filters import SearchFilters
from online_serving.schemas.search_response import SearchResponse, SearchItem

router = APIRouter(prefix="/search", tags=["Search"])
pipeline = SearchPipeline()

@router.get("", response_model=SearchResponse)
def search_products(
    q: str = Query(..., description="Search query"),

    min_price: float | None = Query(None),
    max_price: float | None = Query(None),

    category: str | None = Query(None),
    sub_category: str | None = Query(None),

    min_rating: float | None = Query(None),

    limit: int = Query(10)):
    """
    Search products with filters
    """
    filters = SearchFilters(
        min_price=min_price,
        max_price=max_price,
        category=category,
        sub_category=sub_category,
        min_rating=min_rating
    )
    results, facets, strategy = pipeline.search_products(
        query=q,
        limit=limit,
        filters=filters
    )

    items = []

    for r in results:

        item = SearchItem(
            product_id=r["product_id"],
            title=r["title"],
            gender=r.get("gender", "unknown"),
            final_score=round(r["final_score"], 3)
        )

        items.append(item)

    return SearchResponse(
        query=q,
        total_results=len(items),
        items=items,
        facets=facets,
        strategy_used=strategy
    )