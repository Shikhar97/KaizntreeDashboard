from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http.response import JsonResponse

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


@api_view(['DELETE'])
def delete_stock_item(stock_id=None):
    item = get_object_or_404(Item, id=stock_id)
    try:
        item.delete()
        return JsonResponse({'message': 'Item was deleted successfully!'}, status=204)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@api_view(['GET'])
def list_stock_item(request, stock_id=None):
    query_set = Item.objects.all()

    # Filter by stock status if provided
    stock_status = request.query_params.get('status')
    if stock_status:
        query_set = query_set.filter(stock_status=stock_status)

    # Filter by category if provided
    category = request.query_params.get('category')
    if category:
        query_set = query_set.filter(category=category)

    tags = request.query_params.get('tag')
    if tags:
        tag_ids = tags.split(',')
        query_set = query_set.filter(tags__id__in=tag_ids).distinct()

    if stock_id:
        item = get_object_or_404(query_set, id=stock_id)
        items_serializer = ItemSerializer(item)
    else:
        items_serializer = ItemSerializer(query_set, many=True)

    return JsonResponse(items_serializer.data, safe=False, status=200)

    # elif request.method == 'PUT':
    #     item_data = JSONParser().parse(request)
    #     item = get_object_or_404(Item, id=id)
    #     items_serializer = ItemSerializer(item, data=item_data)
    #     if items_serializer.is_valid():
    #         items_serializer.save()
    #         return JsonResponse(items_serializer.data, safe=False, status=200)
    #     return JsonResponse(items_serializer.errors, status=400)


# @api_view(['GET', 'POST', 'DELETE'])
# def list_category(request, category_id=0):
#     if request.method == 'GET':
#         if id:
#             category = get_object_or_404(Category, id=category_id)
#             categories_serializer = CategorySerializer(category)
#         else:
#             categories = Category.objects.all()
#             categories_serializer = CategorySerializer(categories, many=True)
#         return JsonResponse(categories_serializer.data, safe=False)
#
#     elif request.method == 'POST':
#         category_data = JSONParser().parse(request)
#         categories_serializer = CategorySerializer(data=category_data)
#         if categories_serializer.is_valid():
#             categories_serializer.save()
#             return JsonResponse(categories_serializer.data, safe=False, status=201)
#         return JsonResponse(categories_serializer.errors, safe=False, status=400)
#
#     elif request.method == 'DELETE':
#         category = get_object_or_404(Category, id=id)
#         try:
#             category.delete()
#             return JsonResponse({'message': 'Category was deleted successfully!'}, status=204)
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=400)