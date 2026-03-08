from fastapi import APIRouter, Query, HTTPException
from online_serving.services.recommendation_service import RecommendationService
from firebase.firebase_client import get_products_by_ids

router = APIRouter()
service = RecommendationService()

@router.get("/recommendations")
def get_recommendations(
    last_viewed_product_id: int = Query(...),
    limit: int = Query(10)):
    """
    Get personalized recommendations
    """
    try:
        product_ids = service.get_recommendations(
            user_last_viewed_product_id=last_viewed_product_id,
            limit=limit
        )

        if not product_ids:
            return {"results": []}

        # Fetch product details from Firebase
        products = get_products_by_ids(product_ids)
        return {
            "results": products
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))