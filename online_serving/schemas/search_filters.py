from typing import Optional

class SearchFilters:
    def __init__(
        self,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        category: Optional[str] = None,
        sub_category: Optional[str] = None,
        min_rating: Optional[float] = None,
    ):
        self.min_price = min_price
        self.max_price = max_price
        self.category = category
        self.sub_category = sub_category
        self.min_rating = min_rating