from django.db import models
from products.models import Product
from users.models import User
from django.utils import timezone

class Recommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    score = models.FloatField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Recommendation for {self.user.username} - Product {self.product.id}"
