import pandas as pd
from elasticsearch import Elasticsearch, helpers
from elasticsearch.exceptions import ConnectionError, TransportError

INDEX_NAME = "trendora_products"
DATA_PATH = "data/processed/products_features.parquet"
POPULARITY_PATH = "models/popularity_scores.parquet"

# Connect to elasticsearch
try:
    es = Elasticsearch(
        "http://localhost:9200",
        request_timeout=30,
        verify_certs=False
    )

    if not es.ping():
        raise RuntimeError("Cannot connect to Elasticsearch")

    print("Connected to Elasticsearch")

except ConnectionError:
    raise RuntimeError("Elasticsearch connection failed. Is Docker running?")

except TransportError as e:
    raise RuntimeError(f"Elasticsearch error: {e}")

# Load data
print("Loading product data...")
df = pd.read_parquet(DATA_PATH)

print("Loading popularity scores...")
pop_df = pd.read_parquet(POPULARITY_PATH)

pop_map = dict(zip(pop_df.product_id, pop_df.popularity_score))

print(f"Total products: {len(df)}")

# Bulk indexing
def generate_actions():
    for _, row in df.iterrows():

        yield {
            "_index": INDEX_NAME,
            "_id": row["product_id"],
            "_source": {
                "product_id": int(row["product_id"]),
                "title": row.get("title", ""),
                "description": row.get("description", ""),
                "category": row.get("category", ""),
                "sub_category": row.get("sub_category", ""),
                "gender": row.get("gender", ""),
                "full_text": row.get("full_text", ""),
                "selling_price": float(row.get("selling_price", 0)),
                "discount": float(row.get("discount", 0)),
                "average_rating": float(row.get("average_rating", 0)),
                "popularity_score": float(
                    pop_map.get(row["product_id"], 0.0)
                ),
                "in_stock_flag": int(row.get("in_stock_flag", 1))
            }
        }


# Execute Bulk index

print("Indexing products...")

success, failed = helpers.bulk(
    es,
    generate_actions(),
    chunk_size=1000
)

print(f"Indexed: {success}")
print("Indexing completed successfully!")