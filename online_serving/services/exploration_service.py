import random
from collections import defaultdict

class ExplorationService:
    def __init__(self, exploit_ratio=0.8, seed=42):
        self.exploit_ratio = exploit_ratio
        random.seed(seed)

    def apply_exploration(
        self,
        ranked_items,
        limit=10,
        diversify_by="category"
    ):
        if not ranked_items:
            return []

        exploit_n = int(limit * self.exploit_ratio)
        explore_n = limit - exploit_n

        exploit_items = ranked_items[:exploit_n]
        remaining = ranked_items[exploit_n:]

        if not remaining:
            return exploit_items[:limit]

        explore_items = []

        # Diversity (category, color)
        if diversify_by and diversify_by in remaining[0]:
            groups = defaultdict(list)
            for r in remaining:
                groups[r[diversify_by]].append(r)

            for g in groups:
                explore_items.append(random.choice(groups[g]))
                if len(explore_items) >= explore_n:
                    break
        else:
            explore_items = random.sample(
                remaining,
                k=min(explore_n, len(remaining))
            )

        final = exploit_items + explore_items
        final.sort(key=lambda x: x["final_score"], reverse=True)
        return final[:limit]