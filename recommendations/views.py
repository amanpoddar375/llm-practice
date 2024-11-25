from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Recommendation
from .serializers import RecommendationSerializer
from .recommendation_engine import LLMRecommendationEngine
from products.models import Product

from authentication.bearer_token_authentication import BearerTokenAuthentication


class RecommendProducts(APIView):
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