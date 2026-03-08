from fastapi import APIRouter
from online_serving.services.metadata_service import MetadataService

router = APIRouter()
service = MetadataService()


@router.get("/categories")
def get_categories():
    categories = service.get_categories()
    return {
        "categories": categories
    }

@router.get("/filters")
def get_filters():
    filters = service.get_filters()
    return filters

@router.get("/subcategories")
def get_subcategories():
    """
    Return category -> subcategory mapping
    """
    mapping = service.get_subcategories()
    return {
        "categories": mapping
    }