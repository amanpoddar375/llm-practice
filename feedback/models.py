from django.db import models

# Create your models here.
from django.db import models
from users.models import User
from products.models import Product

class Feedback(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="feedback")
    user_name = models.CharField(max_length=255)
    rating = models.IntegerField()  # Assuming a 1-5 rating system
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_name} - {self.product.name} - {self.rating}"
