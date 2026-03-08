import pandas as pd
from elasticsearch import Elasticsearch, helpers

INDEX_NAME = "trendora_products"
DATA_PATH = "data/processed/products_features.parquet"
POPULARITY_PATH = "models/popularity_scores.parquet"

es = Elasticsearch("http://localhost:9200")

df = pd.read_parquet(DATA_PATH)
pop = pd.read_parquet(POPULARITY_PATH)
pop_map = dict(zip(pop.product_id, pop.popularity_score))

actions = []

for _, row in df.iterrows():
    actions.append({
        "_index": INDEX_NAME,
        "_id": row["product_id"],
        "_source": {
            "product_id": row["product_id"],
            "title": row["title"],
            "description": row["description"],
            "category": row["category"],
            "sub_category": row["sub_category"],
            "gender": row["gender"],
            "full_text": row["full_text"],
            "selling_price": row["selling_price"],
            "discount": row["discount"],
            "average_rating": row["average_rating"],
            "popularity_score": pop_map.get(row["product_id"], 0.0),
            "in_stock_flag": row["in_stock_flag"]
        }
    })

helpers.bulk(es, actions)
print("Products indexed into Elasticsearch")
