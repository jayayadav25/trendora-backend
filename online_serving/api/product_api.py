from fastapi import APIRouter, HTTPException, Query
from online_serving.services.product_service import ProductService

router = APIRouter(prefix="/products", tags=["Products"])
service = ProductService()

@router.get("")
def get_products(
    limit: int = Query(20, description="Number of products to fetch"),
    cursor: str | None = Query(None, description="Pagination cursor")
):
    """
    Get lightweight products for product cards
    Used in:
    - Home screen
    - Category page
    - Recommendation cards
    """

    products = service.get_products(limit=limit, cursor=cursor)
    return {
        "count": len(products),
        "results": products
    }


@router.get("/{product_id}")
def get_product_detail(product_id: str):
    """
    Get full product detail
    Used in Product Detail Page
    """

    product = service.get_product(product_id)
    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )
    return product