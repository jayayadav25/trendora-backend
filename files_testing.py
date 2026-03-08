# from elasticsearch import Elasticsearch

# es = Elasticsearch("http://localhost:9200")
# INDEX = "trendora_products"

# query = "women shirt"

# res = es.search(
#     index=INDEX,
#     query={
#         "multi_match": {
#             "query": query,
#             "fields": ["title^3", "category^2", "description", "full_text"]
#         }
#     },
#     size=5
# )

# print(f"Results for query: '{query}'\n")
# for hit in res["hits"]["hits"]:
#     src = hit["_source"]
#     print(src["product_id"], src["title"], "ES_score:", round(hit["_score"], 3))

# from online_serving.services.search_service import SearchService
# from online_serving.services.search_ranking_service import SearchRankingService

# search = SearchService()
# ranker = SearchRankingService()

# query = "women jewelry"

# hits = search.search(query, size=50)
# ranked = ranker.rank(hits, limit=10)

# print(f"Ranked results for: '{query}'\n")
# for r in ranked:
#     print(
#         r["product_id"],
#         r["title"],
#         "final:", round(r["final_score"], 3),
#         "es:", round(r["es_score"], 3)
#     )

# from online_serving.services.search_service import SearchService
# from online_serving.services.search_ranking_service import SearchRankingService
# from online_serving.services.exploration_service import ExplorationService

# search = SearchService()
# ranker = SearchRankingService()
# explorer = ExplorationService(exploit_ratio=0.8)

# query = "women black shoes"

# hits = search.search(query, size=50)
# ranked = ranker.rank(hits, limit=30)
# final = explorer.apply_exploration(
#     ranked_items=ranked,
#     limit=10,
#     diversify_by="category"
# )

# print(f"Final search results for: '{query}'\n")
# for r in final:
#     print(
#         r["product_id"],
#         r["title"],
#         "final:", round(r["final_score"], 3)
#     )



# from online_serving.services.search_pipeline import SearchPipeline

# pipeline = SearchPipeline()
# results = pipeline.search_products("women shoes", limit=5)

# for r in results:
#     print(f"women shoes{r}")

# from online_serving.services.search_pipeline import SearchPipeline

# pipeline = SearchPipeline()

# queries = [
#     "women earings",

# ]

# for q in queries:
#     print(f"\n🔍 Query: {q}")
#     results = pipeline.search_products(q, limit=5)
#     for r in results:
#         print(f"{r['title']}| product_id={r['product_id']} | gender={r['gender']} | score={round(r['final_score'],3)}")

# from online_serving.services.search_pipeline import SearchPipeline

# pipeline = SearchPipeline()

# queries = [
#     "women shoes",
#     "men blue jacket",
#     "kids shoes",
#     "women accessories",
#     "women earrings",
#     "women pendant",
# ]

# for q in queries:
#     print(f"\n🔍 Query: {q}")
#     results = pipeline.search_products(q, limit=5)
#     for r in results:
#         print(
#             f"{r['title']} | product_id={r['product_id']} | "
#             f"gender={r['gender']} | score={round(r['final_score'],3)}"
#         )

# from online_serving.services.search_pipeline import SearchPipeline
# from online_serving.schemas.search_filters import SearchFilters

# pipeline = SearchPipeline()

# filters = SearchFilters(
#     min_price=500,
#     max_price=2000,
#     min_rating=4.0
# )

# results, facets = pipeline.search_products(
#     query="belt",
#     limit=5,
#     filters=filters
# )

# print("\n🔍 Results:")
# for r in results:
#     print(f"{r['product_id']} | {r['title']} | ₹{r['final_score']:.2f}")

# print("\n📊 Facets:")
# print(facets)

# from online_serving.services.search_pipeline import SearchPipeline


# def run_tests():

#     pipeline = SearchPipeline()

#     test_queries = [
#         "women shoes",
#         "men black jacket",
#         "kids shoes",
#         "women earrings",
#         "women pendant"
#     ]

#     for query in test_queries:
#         print("\n" + "=" * 60)
#         print(f"🔍 Query: {query}")

#         results, aggs = pipeline.search_products(
#             query=query,
#             limit=5,
#             filters=None,
#             user_last_viewed_product_id=42985
#         )

#         if not results:
#             print("❌ No results found")
#             continue

#         for r in results:
#             print(
#                 f"{r['title']} | "
#                 f"product_id={r['product_id']} | "
#                 f"gender={r.get('gender')} | "
#                 f"score={round(r.get('hybrid_score', r['final_score']), 3)}"
#             )

#         # Print facet aggregations if available
#         if aggs:
#             print("\n📊 Facets:")
#             for agg_name, agg_data in aggs.items():
#                 print(f"\n{agg_name.upper()}:")
#                 for bucket in agg_data["buckets"]:
#                     print(f"  {bucket['key']} → {bucket['doc_count']}")


# if __name__ == "__main__":
#     run_tests()


# from online_serving.services.search_pipeline import SearchPipeline
# import random


# def run_tests():

#     pipeline = SearchPipeline()

#     test_queries = [
#         "women shoes",
#         "men black jacket",
#         "kids shoes"
#     ]

#     for query in test_queries:
#         print("\n" + "=" * 60)
#         print(f"🔍 Query: {query}")

#         results, aggs, strategy = pipeline.search_products(
#             query=query,
#             limit=5,
#             user_last_viewed_product_id=42985
#         )

#         print(f"🎯 Strategy Used: {strategy}")

#         if not results:
#             print("❌ No results found")
#             continue

#         for r in results:
#             print(
#                 f"{r['title']} | "
#                 f"product_id={r['product_id']} | "
#                 f"score={round(r.get('hybrid_score', r['final_score']), 3)}"
#             )

#         # 🔥 Simulate click (70% chance on top result)
#         if results and random.random() < 0.7:
#             print("🖱 Simulated Click Recorded")
#             pipeline.record_click(strategy)

#     print("\n📊 Bandit Stats:")
#     print(pipeline.get_bandit_stats())


# if __name__ == "__main__":
#     run_tests()



# import pandas as pd
# df = pd.read_parquet("offline_evaluation/simulated_click_data.parquet")
# print("Rows:", len(df))
# print(df.head())

from firebase.firebase_client import get_products_by_ids

products = get_products_by_ids([42985, 56992])
print(products)