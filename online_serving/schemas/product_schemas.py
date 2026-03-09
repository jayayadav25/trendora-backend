from pydantic import BaseModel
from typing import Optional, List


class ProductCard(BaseModel):
    """
    Lightweight product schema
    Used for product cards
    """

    product_id: str
    title: str

    price: Optional[float] = None
    discount_price: Optional[float] = None

    image_url: Optional[str] = None
    brand: Optional[str] = None

    category: Optional[str] = None
    rating: Optional[float] = None


class ProductDetail(BaseModel):
    """
    Full product schema
    Used in product detail page
    """

    product_id: str
    title: str

    description: Optional[str] = None
    brand: Optional[str] = None

    category: Optional[str] = None
    sub_category: Optional[str] = None

    price: Optional[float] = None
    discount_price: Optional[float] = None

    rating: Optional[float] = None

    images: Optional[List[str]] = None
    sizes: Optional[List[str]] = None
    colors: Optional[List[str]] = None