from django.urls import path
from .views import submit_feedback, get_feedback

urlpatterns = [
    path('submit/', submit_feedback, name='submit_feedback'),
    path('<int:product_id>/', get_feedback, name='get_feedback'),
]
