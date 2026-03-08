from offline_evaluation.click_model import simulate_click


def run_ctr_simulation(pipeline, queries, relevance_labels, k=5, users=100):
    results = []

    for query in queries:
        rel_map = relevance_labels[query]
        clicks = 0
        positions = []

        for _ in range(users):
            ranked = pipeline.search_products(query, limit=k)[0]
            clicked, pos = simulate_click(ranked, rel_map)

            if clicked:
                clicks += 1
                positions.append(pos)

        ctr = clicks / users
        avg_pos = sum(positions) / len(positions) if positions else None

        results.append({
            "query": query,
            "ctr": ctr,
            "avg_click_position": avg_pos
        })

    return results