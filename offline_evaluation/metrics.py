import math


def precision_at_k(results, relevant_ids, k):
    top_k = results[:k]

    hits = sum(
        1 for r in top_k
        if isinstance(r, dict) and r.get("product_id") in relevant_ids
    )

    return hits / k if k else 0


def recall_at_k(results, relevant_ids, k):

    top_k = results[:k]

    hits = sum(
        1 for r in top_k
        if isinstance(r, dict) and r.get("product_id") in relevant_ids
    )

    return hits / len(relevant_ids) if relevant_ids else 0


def dcg_at_k(results, relevant_ids, k):

    dcg = 0.0

    for i, r in enumerate(results[:k]):
        if isinstance(r, dict) and r.get("product_id") in relevant_ids:
            dcg += 1 / math.log2(i + 2)

    return dcg


def ndcg_at_k(results, relevant_ids, k):

    ideal_dcg = sum(
        1 / math.log2(i + 2)
        for i in range(min(len(relevant_ids), k))
    )

    if ideal_dcg == 0:
        return 0

    return dcg_at_k(results, relevant_ids, k) / ideal_dcg