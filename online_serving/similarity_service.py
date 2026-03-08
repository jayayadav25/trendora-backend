from offline_training.similarity.similarity_utils import SimilarityEngine

class SimilarityService:
    def __init__(self):
        self.engine = SimilarityEngine()

    def get_similar_products(self, product_id, k=10):
        return self.engine.similar_by_product_id(product_id, top_k=k)

if __name__ == "__main__":
    service = SimilarityService()
    pid = service.engine.df.iloc[0]["product_id"]
    results = service.get_similar_products(pid, k=5)
    for r in results:
        print(r)
