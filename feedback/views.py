from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from utils.authentication.bearer_token_authentication import BearerTokenAuthentication
from .models import Feedback
from products.models import Product

class SubmitFeedbackView(APIView):
    """
    API endpoint for submitting feedback for a specific product.

    Authentication:
        Requires a valid Bearer Token for the user to submit feedback.

    Permissions:
        Only authenticated users are allowed to access this view.

    HTTP Methods:
        POST: Submit feedback for a product.

    Attributes:
        authentication_classes (list): Specifies the authentication classes used for the view.
        permission_classes (list): Specifies the permission classes used for the view.
    """
    authentication_classes = [BearerTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Handles the submission of feedback for a specific product.
        """
        data = request.data
        product_id = data.get("product_id")
        user_name = data.get("user_name")
        rating = data.get("rating")
        comment = data.get("comment", "")

        try:
            product = Product.objects.get(id=product_id)
            feedback = Feedback.objects.create(
                product=product, user_name=user_name, rating=rating, comment=comment
            )
            return Response({"message": "Feedback submitted successfully!"}, status=201)
        except Product.DoesNotExist:
            return Response({"error": "Product not found."}, status=404)
        
class GetFeedbackView(APIView):
    """
    API endpoint for retrieving feedback for a specific product.

    Authentication:
        Requires a valid Bearer Token for the user to view feedback.

    Permissions:
        Only authenticated users are allowed to access this view.

    HTTP Methods:
        GET: Retrieve feedback for a specific product by its ID.

    Attributes:
        authentication_classes (list): Specifies the authentication classes used for the view.
        permission_classes (list): Specifies the permission classes used for the view.
    """
    authentication_classes = [BearerTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, product_id):
        """
        Retrieves feedback for a specific product.
        """
        try:
            product = Product.objects.get(id=product_id)
            feedback_list = product.feedback.all()
            feedback_data = [
                {
                    "user_name": feedback.user_name,
                    "rating": feedback.rating,
                    "comment": feedback.comment,
                    "created_at": feedback.created_at,
                }
                for feedback in feedback_list
            ]
            return Response({"feedback": feedback_data})
        except Product.DoesNotExist:
            return Response({"error": "Product not found."}, status=404)