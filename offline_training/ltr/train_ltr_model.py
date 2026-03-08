import pandas as pd
import lightgbm as lgb
from pathlib import Path
import joblib
import numpy as np

DATA_PATH = Path("offline_evaluation/simulated_click_data.parquet")
MODEL_PATH = Path("models/ltr_model.txt")

def train_ltr():

    print("Loading training data...")
    df = pd.read_parquet(DATA_PATH)

    if df.empty:
        raise ValueError("Training dataset is empty!")

    feature_cols = [
        "es_score",
        "popularity_score",
        "average_rating",
        "discount"
    ]

    X = df[feature_cols]
    y = df["clicked"]

    # Group by query for ranking
    group = df.groupby("query").size().to_list()

    print("Total rows:", len(df))
    print("Positive clicks:", df["clicked"].sum())

    print("Training LightGBM Ranker...")

    model = lgb.LGBMRanker(
        objective="lambdarank",
        metric="ndcg",
        n_estimators=200,
        learning_rate=0.05,
        min_data_in_leaf=1,
        min_data_in_bin=1
    )

    model.fit( X, y, group=group)

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)

    print("Model:", MODEL_PATH)


if __name__ == "__main__":
    train_ltr()