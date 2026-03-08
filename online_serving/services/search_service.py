from elasticsearch import Elasticsearch
from online_serving.utils.query_parser import extract_gender, normalize_query
from online_serving.schemas.search_filters import SearchFilters

INDEX_NAME = "trendora_products"

class SearchService:
    def __init__(self):
        self.es = Elasticsearch("http://localhost:9200")

    def search(self, query: str, filters: SearchFilters = None, size: int = 50):
        query = normalize_query(query)
        gender = extract_gender(query)

        es_filters = [{"term": {"in_stock_flag": 1}}]

        if gender:
            es_filters.append({"term": {"gender": gender}})

        if filters:
            if filters.category:
                es_filters.append({"term": {"category": filters.category}})
            if filters.sub_category:
                es_filters.append({"term": {"sub_category": filters.sub_category}})
            if filters.min_price or filters.max_price:
                es_filters.append({
                    "range": {
                        "selling_price": {
                            "gte": filters.min_price,
                            "lte": filters.max_price
                        }
                    }
                })
            if filters.min_rating:
                es_filters.append({
                    "range": {
                        "average_rating": {"gte": filters.min_rating}
                    }
                })

        body = {
            "query": {
                "bool": {
                    "must": {
                        "multi_match": {
                            "query": query,
                            "fields": [
                                "title^5",
                                "sub_category^4",
                                "category^3",
                                "full_text"
                            ]
                        }
                    },
                    "filter": es_filters
                }
            },
            "aggs": {
                "category_facet": {
                    "terms": {"field": "category"}
                },
                "sub_category_facet": {
                    "terms": {"field": "sub_category"}
                },
                "price_ranges": {
                    "range": {
                        "field": "selling_price",
                        "ranges": [
                            {"to": 500},
                            {"from": 500, "to": 1000},
                            {"from": 1000, "to": 2000},
                            {"from": 2000}
                        ]
                    }
                }
            },
            "size": size
        }

        return self.es.search(index=INDEX_NAME, body=body)