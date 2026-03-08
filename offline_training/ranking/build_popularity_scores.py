import pandas as pd
from pathlib import Path
from sklearn.preprocessing import MinMaxScaler

DATA_PATH = Path("data/processed/products_features.parquet")
OUTPUT_PATH = Path("models/popularity_scores.parquet")

def build_popularity_scores():
    df = pd.read_parquet(DATA_PATH)

    features = df[[
        "average_rating_norm",
        "discount_norm",
        "selling_price_norm",
        "in_stock_flag",
        "has_image_flag"
    ]].copy()

    features["price_score"] = 1 - features["selling_price_norm"]

    popularity_score = (
        0.40 * features["average_rating_norm"] +
        0.25 * features["discount_norm"] +
        0.15 * features["price_score"] +
        0.10 * features["in_stock_flag"] +
        0.10 * features["has_image_flag"]
    )

    out = df[["product_id"]].copy()
    out["popularity_score"] = popularity_score

    out.to_parquet(OUTPUT_PATH, index=False)
    print("Popularity score:", OUTPUT_PATH)

if __name__ == "__main__":
    build_popularity_scores()
