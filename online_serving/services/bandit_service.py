import random
from collections import defaultdict

class BanditService:

    def __init__(self, epsilon=0.1):
        """
        epsilon = probability of exploration
        """
        self.epsilon = epsilon
        self.stats = defaultdict(lambda: {"clicks": 0, "impressions": 0})

    def choose_strategy(self, strategies):
        """
        strategies: list of strategy names
        """

        # Explore
        if random.random() < self.epsilon:
            return random.choice(strategies)

        # Exploit 
        best_strategy = None
        best_ctr = -1

        for s in strategies:
            impressions = self.stats[s]["impressions"]
            clicks = self.stats[s]["clicks"]

            ctr = clicks / impressions if impressions > 0 else 0

            if ctr > best_ctr:
                best_ctr = ctr
                best_strategy = s

        return best_strategy or random.choice(strategies)

    def record_impression(self, strategy):
        self.stats[strategy]["impressions"] += 1

    def record_click(self, strategy):
        self.stats[strategy]["clicks"] += 1

    def get_stats(self):
        return dict(self.stats)