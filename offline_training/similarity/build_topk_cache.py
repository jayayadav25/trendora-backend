import pandas as pd
import numpy as np
from pathlib import Path
from scipy.sparse import load_npz
from sklearn.metrics.pairwise import cosine_similarity
from tqdm import tqdm


DATA_PATH = Path("data/processed/products_features.parquet")
EMB_PATH = Path("models/product_embeddings_tfidf.npz")
OUTPUT_PATH = Path("models/topk_similar_products.parquet")

TOP_K = 20         
MIN_SIM_SCORE = 0.05

def build_topk_cache():
    print("Loading product data...")
    df = pd.read_parquet(DATA_PATH)

    print("Loading sparse embeddings...")
    embeddings = load_npz(EMB_PATH)

    product_ids = df["product_id"].tolist()
    id_to_index = {pid: idx for idx, pid in enumerate(product_ids)}

    results = []

    print("Building Top-K similarity cache...")
    for idx in tqdm(range(len(product_ids))):
        query_vec = embeddings[idx]

        # cosine similarity with all products
        scores = cosine_similarity(query_vec, embeddings).ravel()

        # remove self similarity
        scores[idx] = -1.0

        top_indices = np.argsort(scores)[::-1][:TOP_K]

        similar_items = []
        for i in top_indices:
            if scores[i] < MIN_SIM_SCORE:
                continue

            similar_items.append({
                "product_id": product_ids[i],
                "score": float(scores[i])
            })

        results.append({
            "product_id": product_ids[idx],
            "similar_products": similar_items
        })

    print("Saving Top-K cache...")
    cache_df = pd.DataFrame(results)
    OUTPUT_PATH.parent.mkdir(exist_ok=True)
    cache_df.to_parquet(OUTPUT_PATH, index=False)

    print("Top-K similarity cache built successfully!")
    print(f"Saved: {OUTPUT_PATH}")
    print(f"Total products cached: {len(cache_df)}")


if __name__ == "__main__":
    build_topk_cache()
