from django.urls import path
from .views import ProductListView, SearchProductsView, CreateProductView

urlpatterns = [
    path("", ProductListView.as_view(), name="product-list"),
    path('search/', SearchProductsView.as_view(), name='search_products'),
    path('create/', CreateProductView.as_view(), name='create-product')
]
