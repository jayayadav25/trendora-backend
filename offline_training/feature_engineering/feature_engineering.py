import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
from pathlib import Path
import json


INPUT_PATH = Path("data/trendora_products.json")
OUTPUT_PATH = Path("data/processed/products_features.parquet")

def load_data(path: Path) -> pd.DataFrame:
    """
    Load product data from JSON file.
    """
    try:
        df = pd.read_json(path)
    except ValueError:
        df = pd.read_json(path, lines=True)

    return df

# Text features

def build_text_feature(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create a single semantic text 
    """
    text_columns = [
        "title",
        "description",
        "category",
        "sub_category",
        "usage",
        "season",
        "baseColour"
    ]

    for col in text_columns:
        if col not in df.columns:
            df[col] = ""

        df[col] = (
            df[col]
            .fillna("")
            .astype(str)
            .str.lower()
            .str.strip()
        )

    df["full_text"] = (
        df["title"] + " " +
        df["description"] + " " +
        df["category"] + " " +
        df["sub_category"] + " " +
        df["usage"] + " " +
        df["season"] + " " +
        df["baseColour"]
    )

    df["full_text"] = df["full_text"].str.replace(r"\s+", " ", regex=True)

    return df


# Numeric features

def build_numeric_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize numeric columns for ranking & popularity
    """
    numeric_cols = [
        "selling_price",
        "discount",
        "average_rating"
    ]

    for col in numeric_cols:
        if col not in df.columns:
            df[col] = 0

        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    scaler = MinMaxScaler()

    df[
        ["selling_price_norm", "discount_norm", "average_rating_norm"]
    ] = scaler.fit_transform(df[numeric_cols])

    return df

# Binary features

def build_binary_features(df: pd.DataFrame) -> pd.DataFrame:
    df["in_stock_flag"] = df.get("in_stock", False).astype(int)
    df["has_image_flag"] = df.get("has_image", False).astype(int)
    return df



# categorical features

def encode_categorical_features(df: pd.DataFrame) -> pd.DataFrame:
    cat_cols = [
        "category",
        "sub_category",
        "baseColour"
    ]

    for col in cat_cols:
        if col not in df.columns:
            df[col] = ""

        le = LabelEncoder()
        df[col + "_encoded"] = le.fit_transform(df[col].astype(str))

    return df

#  main pipeline

def feature_engineering_pipeline():
    print("Loading JSON data...")
    df = load_data(INPUT_PATH)
    print(f"Loaded {len(df)} products")

    print("Building text features...")
    df = build_text_feature(df)

    print("Building numeric features...")
    df = build_numeric_features(df)

    print("Building binary features...")
    df = build_binary_features(df)

    print("Encoding categorical features...")
    df = encode_categorical_features(df)

    print("Saving feature-engineered data...")
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(OUTPUT_PATH, index=False)

    print("Feature engineering completed successfully!")
    print(f"Output: {OUTPUT_PATH}")

    return df

if __name__ == "__main__":
    feature_engineering_pipeline()
