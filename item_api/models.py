from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)


class Item(models.Model):
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sku = models.CharField(max_length=100, default="NULL")
    tag = models.CharField(max_length=100, default="NULL")
    currentStock = models.FloatField(default=0)
    availableStock = models.FloatField(default=0)
    status = models.BooleanField(default=False)
