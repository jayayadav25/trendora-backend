from elasticsearch import Elasticsearch
import time

INDEX_NAME = "trendora_products"

es = Elasticsearch("http://localhost:9200")

print("Waiting for Elasticsearch...")
for _ in range(20):
    if es.ping():
        print("Elasticsearch is ready")
        break
    time.sleep(2)
else:
    raise RuntimeError("Elasticsearch not available")

# Inline synonyms
mapping = {
    "settings": {
        "analysis": {
            "filter": {
                "synonym_filter": {
                    "type": "synonym",
                    "synonyms": [
                        "earring,earrings",
                        "pendent,pendant",
                        "jewelery,jewellery,jewelry",
                        "shoe,shoes,footwear",
                        "sandle,sandles",
                        "dress,dresses",
                        "kurta,kurtis",
                        "kids,kid,boys,girls",
                        "watch,watches,timepiece",
                        "bag,bags,handbag,handbags"
                    ]
                }
            },
            "analyzer": {
                "synonym_text_analyzer": {
                    "tokenizer": "standard",
                    "filter": [
                        "lowercase",
                        "synonym_filter"
                    ]
                }
            }
        }
    },
    "mappings": {
        "properties": {
            "product_id": {"type": "keyword"},
            "title": {
                "type": "text",
                "analyzer": "synonym_text_analyzer"
            },
            "description": {
                "type": "text",
                "analyzer": "synonym_text_analyzer"
            },
            "full_text": {
                "type": "text",
                "analyzer": "synonym_text_analyzer"
            },
            "category": {"type": "keyword"},
            "sub_category": {"type": "keyword"},
            "gender": {"type": "keyword"},
            "selling_price": {"type": "float"},
            "discount": {"type": "float"},
            "average_rating": {"type": "float"},
            "popularity_score": {"type": "float"},
            "in_stock_flag": {"type": "integer"}
        }
    }
}

print("Deleting old index...")
es.indices.delete(index=INDEX_NAME, ignore_unavailable=True)

print("Creating index with inline synonyms...")
es.indices.create(index=INDEX_NAME, body=mapping)

print("Index created successfully!")