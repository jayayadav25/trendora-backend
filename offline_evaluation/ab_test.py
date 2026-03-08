from online_serving.services.search_pipeline import SearchPipeline
from online_serving.services.baseline_ranker import BaselineRanker
from offline_evaluation.click_model import simulate_click

RELEVANCE = {
    "women shoes": {
        42985: 1.0,
        56992: 1.0,
        36331: 0.8,
        51751: 0.7
    },
    "men black jacket": {
        39496: 1.0,
        22312: 0.9,
        59121: 0.8
    }
}

QUERIES = list(RELEVANCE.keys())
USERS = 300
K = 5

pipeline = SearchPipeline()
baseline_ranker = BaselineRanker()

print("\n A/B TEST RESULTS")

for query in QUERIES:
    rel_map = RELEVANCE[query]

    control_clicks = 0
    treatment_clicks = 0

    for _ in range(USERS):
        response = pipeline.search.search(query, size=50)
        hits = response["hits"]["hits"]

        control_ranked = baseline_ranker.rank(hits, K)
        treatment_ranked = pipeline.search_products(query, limit=K)[0]

        c_click, _ = simulate_click(control_ranked, rel_map)
        t_click, _ = simulate_click(treatment_ranked, rel_map)

        if c_click:
            control_clicks += 1
        if t_click:
            treatment_clicks += 1

    control_ctr = control_clicks / USERS
    treatment_ctr = treatment_clicks / USERS

    if control_ctr > 0:
        lift = (treatment_ctr - control_ctr) / control_ctr * 100
        lift_str = f"{lift:.1f}%"
    else:
        lift_str = "N/A (baseline CTR = 0)"

    print(
        f"{query} | "
        f"Control CTR: {control_ctr:.2f}, "
        f"Treatment CTR: {treatment_ctr:.2f}, "
        f"Lift: {lift_str}"
    )