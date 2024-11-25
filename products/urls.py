from django.urls import path
from .views import ProductListView, SearchProductsView

urlpatterns = [
    path("", ProductListView.as_view(), name="product-list"),
    path('search/', SearchProductsView.as_view(), name='search_products'),
]
