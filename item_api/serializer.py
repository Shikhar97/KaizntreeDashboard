from rest_framework import serializers
from .models import Category, Tag, Item

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'