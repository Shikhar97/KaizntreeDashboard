from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)


class Item(models.Model):
    name = models.CharField(max_length=200)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    sku = models.CharField(max_length=12, default="NULL")
    tag = models.CharField(max_length=10, default="NULL")
    currentStock = models.IntegerField(default=0)
    availableStock = models.IntegerField(default=0)
    status = models.BooleanField(default=False)
