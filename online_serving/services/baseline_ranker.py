class BaselineRanker:
    def rank(self, es_hits, limit=10):
        ranked = []

        for h in es_hits:
            src = h["_source"]
            ranked.append({
                "product_id": src["product_id"],
                "final_score": h["_score"]
            })

        ranked.sort(key=lambda x: x["final_score"], reverse=True)
        return ranked[:limit]