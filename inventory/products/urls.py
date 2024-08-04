from django.urls import path
from . import views


app_name = "products"

urlpatterns = [
    path("add/", views.add_product_view, name="add_product_view"),
    path("detail/<product_id>/", views.product_detail_view, name="product_detail_view"),
    path("update/<product_id>/", views.product_update_view, name="product_update_view"),
    path("delete/<product_id>/", views.product_delete_view, name="product_delete_view"),
    path("search/", views.search_products_view, name="search_products_view"),
    path("<category_name>/", views.all_products_view, name="all_products_view"),
    path("reviews/add/<product_id>/", views.add_review_view, name="add_review_view")
]