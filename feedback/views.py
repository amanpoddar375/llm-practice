from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Feedback
from products.models import Product
import json

@csrf_exempt
def submit_feedback(request):
    if request.method == "POST":
        data = json.loads(request.body)
        product_id = data.get("product_id")
        user_name = data.get("user_name")
        rating = data.get("rating")
        comment = data.get("comment", "")

        try:
            product = Product.objects.get(id=product_id)
            feedback = Feedback.objects.create(
                product=product, user_name=user_name, rating=rating, comment=comment
            )
            return JsonResponse({"message": "Feedback submitted successfully!"}, status=201)
        except Product.DoesNotExist:
            return JsonResponse({"error": "Product not found."}, status=404)

    return JsonResponse({"error": "Invalid request method."}, status=405)

def get_feedback(request, product_id):
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
        return JsonResponse({"feedback": feedback_data})
    except Product.DoesNotExist:
        return JsonResponse({"error": "Product not found."}, status=404)
