import random

def simulate_click(results, relevance_map):
    """
    Simulates a single user click based on rank bias.
    Returns clicked product_id or None.
    """

    for i, r in enumerate(results):
        pid = r["product_id"]
        relevance = relevance_map.get(pid, 0)

        # Position bias 
        position_bias = 1 / (i + 1)

        click_prob = relevance * position_bias

        if random.random() < click_prob:
            return pid, i + 1

    return None, None