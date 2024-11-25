from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Recommendation
from .serializers import RecommendationSerializer
from .recommendation_engine import LLMRecommendationEngine
from products.models import Product

from utils.authentication.bearer_token_authentication import BearerTokenAuthentication


class RecommendProducts(APIView):
    """
    RecommendProducts API View

    This view handles personalized product recommendations for authenticated users
    based on their preferences. It uses a recommendation engine to generate
    suggested products, stores the recommendations in the database, and returns
    the serialized data to the user.

    Authentication:
        Requires a valid bearer token.

    Permissions:
        Only authenticated users are allowed to access this view.

    Methods:
        POST: Generates and returns product recommendations.

    Request Payload:
        {
            "user_preferences": "string describing user preferences"
        }

    Args:
        request (Request): The HTTP request object containing user preferences.

    Workflow:
        1. Validates the presence of `user_preferences` in the request payload.
        2. Uses the `LLMRecommendationEngine` to generate product recommendations.
        3. Retrieves corresponding `Product` objects from the database.
        4. Creates `Recommendation` records for each product with a score.
        5. Serializes the created recommendations and returns them.

    Returns:
        Response:
            - On success: A JSON response containing the recommendations and user preferences.
              Example:
              {
                  "recommendations": [
                      {
                          "id": 1,
                          "user": 3,
                          "product": {
                              "id": 101,
                              "name": "Product Name",
                              "category": "Category",
                              ...
                          },
                          "score": 0.95,
                          "created_at": "2024-11-25T12:34:56Z"
                      }
                  ],
                  "user_preferences": "I like technology and gadgets"
              }
            - On input error (status 400): {"error": "User preferences are required"}
            - On server error (status 500): {"error": "Error message"}
    """

    authentication_classes = [BearerTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Generate personalized product recommendations

        Request payload:
        {
            "preferences": "string describing user preferences"
        }
        """
        print(f"Request headers: {request.headers}")
        # Validate input
        user_preferences = request.data.get("user_preferences")
        if not user_preferences:
            return Response(
                {"error": "User preferences are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Initialize recommendation engine
        recommendation_engine = LLMRecommendationEngine()

        try:
            # Generate recommendations
            recommendations = recommendation_engine.generate_recommendations(
                user_preferences=user_preferences
            )

            # Create recommendation records in database
            recommendation_records = []
            for rec in recommendations:
                product = Product.objects.get(id=rec['id'])  # Retrieve the Product object

                recommendation_record = Recommendation.objects.create(
                    user=request.user,
                    product=product,  # Assign the product object
                    score=rec['score']
                )
                recommendation_records.append(recommendation_record)

            # Serialize recommendations
            serializer = RecommendationSerializer(recommendation_records, many=True)

            return Response({
                "recommendations": serializer.data,
                "user_preferences": user_preferences
            })

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )