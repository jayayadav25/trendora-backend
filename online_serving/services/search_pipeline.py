from online_serving.services.search_service import SearchService
from online_serving.services.search_ranking_service import SearchRankingService
from online_serving.services.exploration_service import ExplorationService
from online_serving.services.hybrid_ranking_service import HybridRankingService
from online_serving.services.ranking_service import RankingService
from online_serving.services.bandit_service import BanditService


class SearchPipeline:
    def __init__(self):
        self.search = SearchService()
        self.search_ranker = SearchRankingService()
        self.recommendation_ranker = RankingService()
        self.explorer = ExplorationService(exploit_ratio=0.8)
        self.hybrid = HybridRankingService(self.recommendation_ranker)

        # Bandit for strategy selection
        self.bandit = BanditService(epsilon=0.2)

    def search_products(
        self,
        query,
        limit=10,
        filters=None,
        user_last_viewed_product_id=None
    ):
        """
        Full pipeline:
        - Elasticsearch retrieval
        - Search ranking
        - Bandit selects ranking strategy
        - Exploration
        """

        response = self.search.search(
            query=query,
            filters=filters,
            size=50
        )

        hits = response["hits"]["hits"]

        if not hits:
            return [], {}, None

        # Step 1: Base search ranking
        ranked = self.search_ranker.rank(hits, limit=30)

        # Step 2: Bandit Strategy Selection

        strategies = ["search_only", "hybrid"]

        chosen_strategy = self.bandit.choose_strategy(strategies)

        # Record impression
        self.bandit.record_impression(chosen_strategy)

        if chosen_strategy == "search_only":
            final_ranked = ranked

        elif chosen_strategy == "hybrid":
            final_ranked = self.hybrid.blend(
                ranked,
                user_last_viewed_product_id=user_last_viewed_product_id
            )

        else:
            final_ranked = ranked

        # Step 3: Exploration

        final = self.explorer.apply_exploration(
            ranked_items=final_ranked,
            limit=limit,
            diversify_by="category"
        )

        return final, response.get("aggregations", {}), chosen_strategy

    # Click Recording 

    def record_click(self, strategy_name):
        """
        Call this when a user clicks a product.
        """
        self.bandit.record_click(strategy_name)

    def get_bandit_stats(self):
        """
        Debugging / Monitoring
        """
        return self.bandit.get_stats()