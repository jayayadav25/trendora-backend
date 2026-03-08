from fastapi import FastAPI
from online_serving.api import recommendation_api
from online_serving.api import similar_products_api
from online_serving.api import product_api
from online_serving.api import metadata_api
from online_serving.api import tracking_api
from online_serving.api.search_api import router as search_router

app = FastAPI(
    title="Trendora Search API",
    description="Production-grade eCommerce Search Service",
    version="1.0.0"
)

app.include_router(recommendation_api.router)
app.include_router(similar_products_api.router)
app.include_router(product_api.router)
app.include_router(metadata_api.router)
app.include_router(tracking_api.router)
app.include_router(search_router)



@app.get("/")
def health_check():
    return {"status": "ok"}