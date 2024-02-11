from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Item
from .serializer import ItemSerializer

from django.shortcuts import get_object_or_404


@api_view(['POST'])
def add_stock_item(request):
    items_serializer = ItemSerializer(data=request.data)
    if items_serializer.is_valid():
        items_serializer.save()
        return Response(items_serializer.data, status=status.HTTP_201_CREATED)
    return Response({'message': items_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE'])
def delete_stock_item(request, stock_id):
    item = get_object_or_404(Item, id=stock_id)
    try:
        item.delete()
        return Response({'message': 'Item was deleted successfully!'}, status=status.HTTP_200_OK)
    except Exception as e:
        print(str(e))
        return Response({'message': item.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def list_stock_item(request, stock_id=None):
    query_set = Item.objects.all()

    # Filter by tag
    tag = request.GET.get('tag')
    if tag:
        query_set = query_set.filter(tag=tag)

    # Filter by stock status
    stock_status = request.GET.get('status')
    if stock_status:
        query_set = query_set.filter(status=stock_status)

    # Filter by category
    category = request.GET.get('category')
    if category:
        query_set = query_set.filter(category=category)

    if stock_id:
        item = get_object_or_404(query_set, id=stock_id)
        items_serializer = ItemSerializer(item)
    else:
        items_serializer = ItemSerializer(query_set, many=True)

    return Response(items_serializer.data, status=status.HTTP_200_OK)
