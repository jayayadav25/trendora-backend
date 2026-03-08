from online_serving.services.ranking_service import RankingService


class RecommendationService:
    """
    Recommendation layer.
    Returns ranked product_ids.
    """

    def __init__(self):
        self.ranker = RankingService()

    def get_recommendations(self, user_last_viewed_product_id: int, limit: int = 10):
        """
        Returns ranked product IDs
        """

        if not user_last_viewed_product_id:
            return []

        ranked = self.ranker.rank_similar_products(
            product_id=user_last_viewed_product_id,
            limit=limit
        )

        return [r["product_id"] for r in ranked]