from django.db import models

# Create your models here.
from django.db import models
from users.models import User
from products.models import Product

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    feedback = models.TextField()

    def __str__(self):
        return f"Feedback by {self.user.username}"
