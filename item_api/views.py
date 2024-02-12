from datetime import datetime

from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from .models import Item, Category
from .serializer import ItemSerializer, CategorySerializer

from django.shortcuts import get_object_or_404
from django.core.cache import cache
import redis
from rest_framework.response import Response
redis_instance = redis.StrictRedis(host='127.0.0.1', port=6379)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_stock_item(request):
    """

    :param request:
    :return:
    """
    items_serializer = ItemSerializer(data=request.data)
    if items_serializer.is_valid():
        items_serializer.save()
        return Response(items_serializer.data, status=status.HTTP_201_CREATED)
    return Response({'message': items_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_stock_item(request, stock_id=None):
    query_set = Item.objects.all()

    # Filter by date range
    created_after = request.GET.get('created_after')
    created_before = request.GET.get('created_before')
    if created_after and created_before:
        created_after = datetime.strptime(created_after, "%Y-%m-%d")
        created_before = datetime.strptime(created_before, "%Y-%m-%d")
        query_set = query_set.filter(createdAt__gte=created_after, createdAt__lte=created_before)

    # Filter by stock status
    stock_status = request.GET.get('status')
    if stock_status:
        query_set = query_set.filter(status=stock_status)

    # Filter by category
    category = request.GET.get('category')
    if category:
        query_set = query_set.filter(category=category)

    # Caching results
    if stock_id:
        item = get_object_or_404(query_set, id=stock_id)
        items_serializer = ItemSerializer(item)
        cache_key = f'item:{items_serializer.data}'
        if cache_key in cache:
            return Response(cache.get(cache_key), status=status.HTTP_200_OK)

        cache.set(cache_key, items_serializer.data, timeout=(60 * 5))
        return Response(items_serializer.data, status=status.HTTP_200_OK)
    else:
        paginator = PageNumberPagination()
        paginator.page_size = 5
        queryset = paginator.paginate_queryset(query_set, request)
        items_serializer = ItemSerializer(queryset, many=True)
        cache_key = f'item:{items_serializer.data}'
        if cache_key in cache:
            return paginator.get_paginated_response(cache.get(cache_key))

        cache.set(cache_key, items_serializer.data, timeout=(60 * 5))
        return paginator.get_paginated_response(items_serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_stock_item(request, stock_id=None):
    """

    :param request:
    :param stock_id:
    :return:
    """
    item = get_object_or_404(Item, id=stock_id)
    try:
        item.delete()
        return Response({'message': 'Item was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({'message': item.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_category(request):
    categories_serializer = CategorySerializer(data=request.data)
    if categories_serializer.is_valid():
        categories_serializer.save()
        return Response(categories_serializer.data, status=status.HTTP_201_CREATED)
    return Response({'message': categories_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_category(request, category_name=None):
    category = get_object_or_404(Category, name=category_name)
    try:
        category.delete()
        return Response({'message': 'Category was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({'message': category.errors}, status=status.HTTP_400_BAD_REQUEST)
