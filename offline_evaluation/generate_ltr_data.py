from online_serving.services.search_pipeline import SearchPipeline
import pandas as pd
import random
from pathlib import Path

OUTPUT_PATH = Path("offline_evaluation/simulated_click_data.parquet")

def generate_data():

    pipeline = SearchPipeline()

    queries = [
        "women shoes",
        "men black jacket",
        "kids shoes",
        "women kurta",
        "women watch",
        "men t-shirt",
        "women jewelry",
        "accessiories",
        "beauty products",
        "men perfume",
        "kids dresses"
    ]

    rows = []

    # Generate more data
    for _ in range(30): 

        for query in queries:

            results, _, _ = pipeline.search_products(
                query=query,
                limit=10
            )

            if not results:
                continue

            for rank, r in enumerate(results):

                # Rank-based click probability
                click_prob = 1 / (rank + 1)

                clicked = 1 if random.random() < click_prob else 0

                rows.append({
                    "query": query,
                    "product_id": r["product_id"],
                    "es_score": r["es_score"],
                    "popularity_score": r["popularity_score"],
                    "average_rating": random.uniform(3.0, 5.0),
                    "discount": random.uniform(0, 50),
                    "clicked": clicked
                })

    df = pd.DataFrame(rows)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(OUTPUT_PATH, index=False)

    print("Training data saved to:", OUTPUT_PATH)
    print("Total rows generated:", len(df))


if __name__ == "__main__":
    generate_data()