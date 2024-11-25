from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.db.models import Q
# Create your views here.
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from authentication.bearer_token_authentication import BearerTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Product
from .serializers import ProductSerializer

class ProductListView(generics.ListCreateAPIView):
    authentication_classes = [BearerTokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class SearchProductsView(APIView):
    authentication_classes = [BearerTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = request.GET.get('q', '')  # Get the search query from the request
        if query:
            products = Product.objects.filter(
                Q(name__icontains=query) |
                Q(category__icontains=query) |
                Q(description__icontains=query)
            )
        else:
            products = Product.objects.all()

        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)