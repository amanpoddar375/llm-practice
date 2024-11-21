from django.db import models

# Create your models here.
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    description = models.TextField()
    price = models.FloatField()
    metadata = models.JSONField(null=True, blank=True)

    def __str__(self):
        return self.name
