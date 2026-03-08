import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib


DATA_PATH = Path("data/processed/products_features.parquet")
MODEL_DIR = Path("models")
TFIDF_PATH = MODEL_DIR / "tfidf_vectorizer.pkl"


def train_tfidf():
    print("Loading feature-engineered data...")
    df = pd.read_parquet(DATA_PATH)

    texts = df["full_text"].fillna("").tolist()

    print("Training TF-IDF vectorizer...")
    tfidf = TfidfVectorizer(
        max_features=30000,
        ngram_range=(1, 2),
        min_df=2,
        stop_words="english"
    )

    tfidf.fit(texts)

    MODEL_DIR.mkdir(exist_ok=True)
    joblib.dump(tfidf, TFIDF_PATH)

    print("TF-IDF training completed")
    print(f"Saved: {TFIDF_PATH}")

    return tfidf

if __name__ == "__main__":
    train_tfidf()
