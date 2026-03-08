import pandas as pd
from pathlib import Path
import joblib
from sklearn.preprocessing import normalize
from scipy.sparse import save_npz

DATA_PATH = Path("data/processed/products_features.parquet")
MODEL_DIR = Path("models")
TFIDF_PATH = MODEL_DIR / "tfidf_vectorizer.pkl"
EMBEDDING_PATH = MODEL_DIR / "product_embeddings_tfidf.npz"

def build_embeddings():
    print("Loading feature-engineered data...")
    df = pd.read_parquet(DATA_PATH)

    print("Loading TF-IDF model...")
    tfidf = joblib.load(TFIDF_PATH)

    print("Transforming text into TF-IDF vectors (SPARSE)...")
    text_vectors = tfidf.transform(df["full_text"].fillna(""))

    print("Normalizing vectors (L2, sparse-safe)...")
    embeddings = normalize(text_vectors, norm="l2")

    MODEL_DIR.mkdir(exist_ok=True)

    print("Saving sparse embeddings (.npz)...")
    save_npz(EMBEDDING_PATH, embeddings)

    print("Sparse product embeddings saved successfully")
    print(f"Path: {EMBEDDING_PATH}")
    print(f"Shape: {embeddings.shape}")

    return embeddings

if __name__ == "__main__":
    build_embeddings()
