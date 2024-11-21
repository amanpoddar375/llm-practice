from django.urls import path
from .views import RecommendProducts

urlpatterns = [
    path("recommend/", RecommendProducts.as_view(), name="recommend-products"),
]