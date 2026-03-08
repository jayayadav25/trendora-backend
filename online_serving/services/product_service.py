from firebase.firebase_client import ( get_products_light, get_product_detail)

class ProductService:
    """
    Handles product data.
    Fetches products from Firebase.
    """

    def get_products(self, limit: int = 20, cursor: str | None = None):
        """
        Fetch products for product cards
        """
        products = get_products_light(limit=limit, start_after=cursor)
        return products

    def get_product(self, product_id: str):
        """
        Fetch full product detail
        """
        product = get_product_detail(product_id)
        return product