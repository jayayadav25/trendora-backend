from online_serving.services.ranking_service import RankingService


class SimilarProductsService:
    """
    Service for retrieving similar products
    using content-based filtering.
    """

    def __init__(self):
        self.ranker = RankingService()

    def get_similar_products(self, product_id: int, limit: int = 10):
        """
        Returns ranked similar product_ids
        """

        ranked = self.ranker.rank_similar_products(
            product_id=product_id,
            limit=limit
        )

        return [r["product_id"] for r in ranked]