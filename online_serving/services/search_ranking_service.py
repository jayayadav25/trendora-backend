class SearchRankingService:
    
    def rank(self, es_hits, limit=30):
        if not es_hits:
            return []

        ranked = []
        max_es_score = max(h["_score"] for h in es_hits if h["_score"] is not None)

        for h in es_hits:
            src = h["_source"]

            es_score_norm = h["_score"] / max_es_score if max_es_score else 0

            final_score = (
                0.5 * es_score_norm +
                0.3 * src.get("popularity_score", 0.0) +
                0.1 * (src.get("average_rating", 0.0) / 5.0) +
                0.1 * (src.get("discount", 0.0) / 100.0)
            )

            ranked.append({
                "product_id": src["product_id"],
                "title": src["title"],
                "category": src.get("category"),
                "gender": src.get("gender"),
                "final_score": final_score,
                "es_score": h["_score"],
                "similarity_score": es_score_norm,
                "popularity_score": src.get("popularity_score", 0.0)
            })

        ranked.sort(key=lambda x: x["final_score"], reverse=True)
        return ranked[:limit]