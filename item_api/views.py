from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from django.http.response import JsonResponse, HttpResponse

from .models import Category, Tag, Item
from .serializer import CategorySerializer, TagSerializer, ItemSerializer

from django.core.files.storage import default_storage
from django.shortcuts import get_object_or_404


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def dashboardApi(request, id=None):
    if request.method == 'GET':
        query_set = Item.objects.all()

        # Filter by stock status if provided
        stock_status = request.query_params.get('stock_status')
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

        if id:
            item = get_object_or_404(query_set, id=id)
            items_serializer = ItemSerializer(item)
        else:
            items_serializer = ItemSerializer(query_set, many=True)

        return JsonResponse(items_serializer.data, safe=False, status=200)

    elif request.method == 'POST':
        item_data = JSONParser().parse(request)
        items_serializer = ItemSerializer(data=item_data)
        if items_serializer.is_valid():
            items_serializer.save()
            return JsonResponse(items_serializer.data, safe=False, status=201)
        return JsonResponse(items_serializer.errors, safe=False, status=400)

    elif request.method == 'PUT':
        item_data = JSONParser().parse(request)
        item = get_object_or_404(Item, id=id)
        items_serializer = ItemSerializer(item, data=item_data)
        if items_serializer.is_valid():
            items_serializer.save()
            return JsonResponse(items_serializer.data, safe=False, status=200)
        return JsonResponse(items_serializer.errors, status=400)

    elif request.method == 'DELETE':
        item = get_object_or_404(Item, id=id)
        try:
            item.delete()
            return JsonResponse({'message': 'Item was deleted successfully!'}, status=204)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


@api_view(['GET', 'POST', 'DELETE'])
def categoryApi(request, id=0):
    if request.method == 'GET':
        if id:
            category = get_object_or_404(Category, id=id)
            categories_serializer = CategorySerializer(category)
        else:
            categories = Category.objects.all()
            categories_serializer = CategorySerializer(categories, many=True)
        return JsonResponse(categories_serializer.data, safe=False)

    elif request.method == 'POST':
        category_data = JSONParser().parse(request)
        categories_serializer = CategorySerializer(data=category_data)
        if categories_serializer.is_valid():
            categories_serializer.save()
            return JsonResponse(categories_serializer.data, safe=False, status=201)
        return JsonResponse(categories_serializer.errors, safe=False, status=400)

    elif request.method == 'DELETE':
        category = get_object_or_404(Category, id=id)
        try:
            category.delete()
            return JsonResponse({'message': 'Category was deleted successfully!'}, status=204)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


@api_view(['GET', 'POST', 'DELETE'])
def tagApi(request, id=0):
    if request.method == 'GET':
        if id:
            tag = get_object_or_404(Tag, id=id)
            tags_serializer = TagSerializer(tag)
        else:
            tags = Tag.objects.all()
            tags_serializer = TagSerializer(tags, many=True)
        return JsonResponse(tags_serializer.data, safe=False)

    elif request.method == 'POST':
        tag_data = JSONParser().parse(request)
        tags_serializer = TagSerializer(data=tag_data)
        if tags_serializer.is_valid():
            tags_serializer.save()
            return JsonResponse(tags_serializer.data, safe=False, status=201)
        return JsonResponse(tags_serializer.errors, safe=False, status=400)

    elif request.method == 'DELETE':
        tag = get_object_or_404(Tag, id=id)
        try:
            tag.delete()
            return JsonResponse({'message': 'Tag was deleted successfully!'}, status=204)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)