from rest_framework import serializers
from .models import Recommendation
from products.serializers import ProductSerializer

class RecommendationSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Recommendation
        fields = ['id', 'user', 'product', 'score', 'created_at']