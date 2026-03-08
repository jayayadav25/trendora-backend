import pandas as pd
from pathlib import Path

TOPK_PATH = Path("models/topk_similar_products.parquet")
POPULARITY_PATH = Path("models/popularity_scores.parquet")


class RankingService:
    def __init__(self):
        self.topk_df = pd.read_parquet(TOPK_PATH)
        self.pop_df = pd.read_parquet(POPULARITY_PATH)

        self.pop_map = dict(
            zip(self.pop_df.product_id, self.pop_df.popularity_score)
        )

    def rank_similar_products(self, product_id, limit=50):

        row = self.topk_df[self.topk_df.product_id == product_id]

        if row.empty:
            return []

        candidates = row.iloc[0]["similar_products"]

        ranked = []

        for c in candidates:
            pid = c["product_id"]
            sim_score = c["score"]
            pop_score = self.pop_map.get(pid, 0.0)

            final_score = 0.65 * sim_score + 0.35 * pop_score

            ranked.append({
                "product_id": pid,
                "similarity_score": sim_score,
                "popularity_score": pop_score,
                "final_score": final_score
            })

        ranked.sort(key=lambda x: x["final_score"], reverse=True)
        return ranked[:limit]