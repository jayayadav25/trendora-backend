from fastapi import APIRouter, HTTPException
from online_serving.services.similar_products_service import SimilarProductsService
from firebase.firebase_client import get_products_by_ids

router = APIRouter()
service = SimilarProductsService()

@router.get("/products/{product_id}/similar")
def get_similar_products(product_id: int, limit: int = 10):
    """
    Get similar products based on content similarity
    """

    try:
        product_ids = service.get_similar_products(product_id, limit)
        if not product_ids:
            return {"results": []}

        products = get_products_by_ids(product_ids)
        return {
            "results": products
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))