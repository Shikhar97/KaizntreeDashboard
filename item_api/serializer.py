from rest_framework import serializers
from .models import Category, Tag, Item


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')


class ItemSerializer(serializers.ModelSerializer):
    # Add nested serializers
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), write_only=True)
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True, write_only=True)

    class Meta:
        model = Item
        fields = ('id', 'sku', 'name', 'category', 'tags', 'stock_status', 'available_stock')

    def to_representation(self, instance):
        # Use the read-only serializers for reading
        representation = super(ItemSerializer, self).to_representation(instance)
        representation['category'] = CategorySerializer(instance.category).data
        representation['tags'] = TagSerializer(instance.tags, many=True).data
        return representation

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        item = Item.objects.create(**validated_data)
        item.tags.set(tags_data)  # Associate the tags using set()
        return item