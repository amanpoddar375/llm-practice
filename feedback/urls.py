from django.urls import path
from .views import GetFeedbackView, SubmitFeedbackView
urlpatterns = [
    path('submit/', SubmitFeedbackView.as_view(), name='submit_feedback'),
    path('<int:product_id>/', GetFeedbackView.as_view(), name='get_feedback'),
]