from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionError, TransportError

INDEX_NAME = "trendora_products"

es = Elasticsearch( "http://localhost:9200",  request_timeout=30, verify_certs=False)

# Index mapping

mapping = {
    "settings": {
        "analysis": {
            "analyzer": {
                "text_analyzer": {
                    "type": "standard",
                    "stopwords": "_english_"
                }
            }
        }
    },
    "mappings": {
        "properties": {
            "product_id": {"type": "keyword"},
            "title": {"type": "text", "analyzer": "text_analyzer"},
            "description": {"type": "text", "analyzer": "text_analyzer"},
            "category": {"type": "keyword"},
            "sub_category": {"type": "keyword"},
            "gender": {"type": "keyword"},
            "full_text": {"type": "text", "analyzer": "text_analyzer"},
            "selling_price": {"type": "float"},
            "discount": {"type": "float"},
            "average_rating": {"type": "float"},
            "popularity_score": {"type": "float"},
            "in_stock_flag": {"type": "integer"}
        }
    }
}

try:
    print(f"Deleting index if exists: {INDEX_NAME}")
    es.indices.delete(index=INDEX_NAME, ignore=[404])

    print(f"Creating index: {INDEX_NAME}")
    es.indices.create(index=INDEX_NAME, body=mapping)

    print("Elasticsearch index created successfully")

except ConnectionError:
    raise RuntimeError(
        "Cannot connect to Elasticsearch at http://localhost:9200\n"
        "Make sure Docker container is running"
    )

except TransportError as e:
    raise RuntimeError(f"Elasticsearch error: {e}")