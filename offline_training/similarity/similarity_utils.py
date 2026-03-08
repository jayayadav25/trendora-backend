import numpy as np
import pandas as pd
from scipy.sparse import load_npz
from sklearn.metrics.pairwise import cosine_similarity
from pathlib import Path

DATA_PATH = Path("data/processed/products_features.parquet")
EMB_PATH = Path("models/product_embeddings_tfidf.npz")

class SimilarityEngine:
    def __init__(self):
        self.df = pd.read_parquet(DATA_PATH)
        self.emb = load_npz(EMB_PATH)

        # map product_id -> row index
        self.pid_to_idx = {
            pid: i for i, pid in enumerate(self.df["product_id"].tolist())
        }

    def similar_by_product_id(self, product_id, top_k=10, min_score=0.05):
        if product_id not in self.pid_to_idx:
            return []

        q_idx = self.pid_to_idx[product_id]
        q_vec = self.emb[q_idx]

        # cosine similarity with sparse matrix
        scores = cosine_similarity(q_vec, self.emb).ravel()

        # exclude itself
        scores[q_idx] = -1.0

        top_idx = np.argsort(scores)[::-1][:top_k]
        results = []

        for i in top_idx:
            if scores[i] < min_score:
                continue
            row = self.df.iloc[i]
            results.append({
                "product_id": row["product_id"],
                "title": row["title"],
                "category": row["category"],
                "score": float(scores[i])
            })

        return results
