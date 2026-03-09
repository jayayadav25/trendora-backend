import os
import json
import base64
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

cred = None

# Try Base64 environment variable (Render)
firebase_base64 = os.getenv("FIREBASE_SERVICE_ACCOUNT_BASE64")

if firebase_base64:
    firebase_json = base64.b64decode(firebase_base64).decode("utf-8")
    firebase_dict = json.loads(firebase_json)
    cred = credentials.Certificate(firebase_dict)

# Fallback to local file
else:
    cred = credentials.Certificate("firebase/serviceAccountKey.json")

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()

# Extract image URL

def extract_image(images):

    if not images:
        return None

    # Case 1 → list of objects
    if isinstance(images, list):

        first = images[0]

        if isinstance(first, dict):
            return first.get("url")

        if isinstance(first, str):
            return first

    # Case 2 → dictionary
    if isinstance(images, dict):

        if "original" in images:
            return images["original"]

        return list(images.values())[0]

    return None

# Products for product cards (lightweight)

def get_products_light(limit=20, start_after=None):

    query = db.collection("products_light").limit(limit)

    docs = query.stream()

    products = []

    for doc in docs:
        data = doc.to_dict()
        data["product_id"] = doc.id
        products.append(data)

    return products

# Product detail

def get_product_detail(product_id):
    doc = db.collection("products").document(str(product_id)).get()
    if not doc.exists:
        return None

    product = doc.to_dict()
    product["product_id"] = product_id
    return product

# Multiple products(recommendations/search)

def get_products_by_ids(product_ids):

    products = []

    for pid in product_ids:
        doc = db.collection("products_light").document(str(pid)).get()
        if doc.exists:
            data = doc.to_dict()
            data["product_id"] = pid
            products.append(data)

    return products

# products by categories
def get_all_categories():
    """
    Fetch unique categories from products_light
    """
    docs = db.collection("products_light").stream()
    categories = set()

    for doc in docs:
        data = doc.to_dict()

        if "category" in data:
            categories.add(data["category"])

    return list(categories)

# Filter categories 

def get_filter_metadata():
    """
    Extract brands, categories, and price ranges
    """
    docs = db.collection("products_light").stream()

    categories = set()
    brands = set()
    prices = []

    for doc in docs:
        data = doc.to_dict()
        if "category" in data:
            categories.add(data["category"])

        if "brand" in data:
            brands.add(data["brand"])

        if "price" in data:
            prices.append(data["price"])

    if prices:
        min_price = min(prices)
        max_price = max(prices)
    else:
        min_price = 0
        max_price = 0

    return {
        "categories": list(categories),
        "brands": list(brands),
        "price_range": {
            "min": min_price,
            "max": max_price
        }
    }

# Filter subcategories

def get_category_subcategories():
    """
    Fetch category -> subcategory mapping
    """

    docs = db.collection("products_light").stream()
    category_map = {}

    for doc in docs:
        data = doc.to_dict()
        category = data.get("category")
        sub_category = data.get("sub_category")

        if not category or not sub_category:
            continue

        if category not in category_map:
            category_map[category] = set()

        category_map[category].add(sub_category)

    # convert sets to list
    for k in category_map:
        category_map[k] = list(category_map[k])

    return category_map


# Event tracking


def log_event(collection_name: str, data: dict):
    """
    Generic event logger for ML tracking
    """

    try:
        data["timestamp"] = datetime.utcnow()
        db.collection(collection_name).add(data)

    except Exception as e:
        print(f"Firestore logging error: {e}")