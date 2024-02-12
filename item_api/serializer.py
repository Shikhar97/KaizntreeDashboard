from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Item, Category


class CustomPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    def to_internal_value(self, data):
        try:
            return super().to_internal_value(data)
        except ValidationError as e:
            raise ValidationError("Invalid category, does not exist.") from e


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class ItemSerializer(serializers.ModelSerializer):
    category = CustomPrimaryKeyRelatedField(queryset=Category.objects.all(), write_only=True)

    class Meta:
        model = Item
        fields = '__all__'

    def to_representation(self, instance):
        representation = super(ItemSerializer, self).to_representation(instance)
        representation['category'] = CategorySerializer(instance.category).data
        return representation

    def create(self, validated_data):
        category_data = validated_data.pop('category')
        item = Item.objects.create(**validated_data, category=category_data)
        return item
