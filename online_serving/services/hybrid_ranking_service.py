class HybridRankingService:

    def __init__(self, recommendation_service):
        self.recommendation_service = recommendation_service

    def blend( self, search_ranked,  user_last_viewed_product_id=None,
        alpha=0.6,  beta=0.3,  gamma=0.1 ):
        """
        Hybrid blending:
        - Search relevance
        - Product similarity
        - Popularity
        """

        if not search_ranked:
            return []

        similarity_map = {}

        # If user context exists
        if user_last_viewed_product_id:
            similar_products = self.recommendation_service.rank_similar_products(
                user_last_viewed_product_id,
                limit=50
            )

            similarity_map = {
                p["product_id"]: p["final_score"]
                for p in similar_products
            }

        blended = []

        for item in search_ranked:

            search_score = item["final_score"]
            similarity_score = similarity_map.get(item["product_id"], 0.0)
            popularity_score = item.get("popularity_score", 0.0)

            hybrid_score = (
                alpha * search_score +
                beta * similarity_score +
                gamma * popularity_score
            )

            item["hybrid_score"] = hybrid_score
            blended.append(item)

        blended.sort(key=lambda x: x["hybrid_score"], reverse=True)
        return blended