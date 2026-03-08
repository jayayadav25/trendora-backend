from firebase.firebase_client import log_event


class TrackingService:

    def track_search(self, user_id: str, query: str):
        log_event("search_events", {
            "user_id": user_id,
            "query": query
        })

    def track_click(
        self,
        user_id: str,
        product_id: int,
        query: str,
        position: int
    ):
        log_event("click_events", {
            "user_id": user_id,
            "product_id": product_id,
            "query": query,
            "position": position
        })

    def track_add_to_cart(
        self,
        user_id: str,
        product_id: int
    ):
        log_event("cart_events", {
            "user_id": user_id,
            "product_id": product_id
        })