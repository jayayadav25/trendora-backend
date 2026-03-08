import json
from online_serving.services.search_pipeline import SearchPipeline
from offline_evaluation.metrics import precision_at_k, recall_at_k, ndcg_at_k

pipeline = SearchPipeline()

with open("offline_evaluation/sample_queries.json") as f:
    test_cases = json.load(f)

K = 5


def normalize_results(results):
    """
    Flatten nested results and keep only valid product dictionaries
    """
    normalized = []

    for r in results:
        # case 1: correct dict
        if isinstance(r, dict) and "product_id" in r:
            normalized.append(r)

        # case 2: nested list
        elif isinstance(r, list):
            for item in r:
                if isinstance(item, dict) and "product_id" in item:
                    normalized.append(item)

    return normalized


for case in test_cases:

    query = case["query"]
    relevant_ids = case["relevant_product_ids"]

    # pipeline returns tuple
    results, facets, strategy = pipeline.search_products(query=query, limit=K)

    results = normalize_results(results)

    p = precision_at_k(results, relevant_ids, K)
    r = recall_at_k(results, relevant_ids, K)
    n = ndcg_at_k(results, relevant_ids, K)

    print("\nQuery:", query)
    print("Strategy:", strategy)
    print(f"Precision@{K}: {p:.2f}")
    print(f"Recall@{K}: {r:.2f}")
    print(f"NDCG@{K}: {n:.2f}")