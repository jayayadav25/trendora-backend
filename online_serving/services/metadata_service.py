from firebase.firebase_client import (  get_all_categories, get_category_subcategories, get_filter_metadata)

class MetadataService:

    def get_categories(self):
        return get_all_categories()

    def get_filters(self):
        return get_filter_metadata()
    
    def get_subcategories(self):
        return get_category_subcategories()