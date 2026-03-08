from fastapi import APIRouter
from pydantic import BaseModel
from online_serving.services.tracking_service import TrackingService

router = APIRouter()
service = TrackingService()

# Request Schemas

class SearchEvent(BaseModel):
    user_id: str
    query: str


class ClickEvent(BaseModel):
    user_id: str
    product_id: int
    query: str
    position: int


class CartEvent(BaseModel):
    user_id: str
    product_id: int


# Endpoints 

@router.post("/track/search")
def track_search(event: SearchEvent):
    service.track_search(event.user_id, event.query)
    return {"status": "search tracked"}


@router.post("/track/click")
def track_click(event: ClickEvent):
    service.track_click(
        event.user_id,
        event.product_id,
        event.query,
        event.position
    )
    return {"status": "click tracked"}


@router.post("/track/cart")
def track_cart(event: CartEvent):
    service.track_add_to_cart(
        event.user_id,
        event.product_id
    )
    return {"status": "cart event tracked"}