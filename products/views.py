from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.db.models import Q
# Create your views here.
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from utils.authentication.bearer_token_authentication import BearerTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Product
from .serializers import ProductSerializer


class CreateProductView(APIView):
    """
    Handles the creation of a new product.

    This view accepts product data in the request body, validates it using the
    ProductSerializer, and saves it to the database if valid.

    Authentication:
        Requires a valid bearer token.

    Permissions:
        Only authenticated users are allowed to access this view.

    Methods:
        post(request): Creates a new product.

    Args:
        request (Request): The HTTP request containing product data.

    Returns:
        Response: A JSON response with the created product's data (status 201),
                  or validation errors (status 400).
    """

    authentication_classes = [BearerTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductListView(generics.ListCreateAPIView):
    """
    Handles listing all products or creating a new product.

    This view provides both list and create functionalities for products.
    It uses `generics.ListCreateAPIView` for a combined interface.

    Authentication:
        Requires a valid bearer token.

    Permissions:
        Only authenticated users are allowed to access this view.

    Attributes:
        queryset (QuerySet): All product objects in the database.
        serializer_class (Serializer): The serializer used for product data.

    Methods:
        GET: Lists all products.
        POST: Creates a new product.
    """

    authentication_classes = [BearerTokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class SearchProductsView(APIView):
    """
    Handles searching for products based on a query.

    This view allows authenticated users to search for products by their
    name, category, or description using a query parameter `q`.

    Authentication:
        Requires a valid bearer token.

    Permissions:
        Only authenticated users are allowed to access this view.

    Methods:
        get(request): Searches for products matching the query.

    Args:
        request (Request): The HTTP request containing the query parameter `q`.

    Returns:
        Response: A JSON response with the list of matching products.
    """

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