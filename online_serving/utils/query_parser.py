import re

# Gender
def extract_gender(query: str):
    q = query.lower()

    if re.search(r"\bwomen\b|\bfemale\b|\bladies\b|\bgirls\b", q):
        return "women"
    if re.search(r"\bmen\b|\bmale\b|\bboys\b", q):
        return "men"
    if re.search(r"\bkid\b|\bkids\b|\bchild\b", q):
        return "kids"

    return None


# Query normalization

def normalize_query(query: str):
    q = query.lower()

    replacements = {
        "dress": "dresses",
        "sandle": "sandles",
        "earings": "earrings",
        "earing": "earrings",
        "pendant": "pendants",
        "pendents": "pendants",
        "jewelery": "jewelry",
    }

    for wrong, correct in replacements.items():
        q = q.replace(wrong, correct)

    return q


# category/subcategory
def extract_category_intent(query: str):
    q = query.lower()

    # Jewelry
    if re.search(r"jewel|earring|earrings|pendant|pendants|necklace|locket", q):
        return {
            "category": "accessories",
            "sub_categories": [
                "earrings",
                "pendants",
                "necklace",
                "locket",
                "jewellery"
            ]
        }

    # Belts
    if re.search(r"belt|belts", q):
        return {
            "category": "accessories",
            "sub_categories": ["belt", "belts"]
        }

    # Shoes
    if re.search(r"shoe|shoes|sneaker|sandals|sandles|heels", q):
        return {
            "category": "shoes"
        }

    return {}