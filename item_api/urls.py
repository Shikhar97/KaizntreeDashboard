from django.urls import path
from . import views

urlpatterns = [
    path("list/", views.list_stock_item, name='list'),
    path("add/", views.add_stock_item, name='add'),
    path('list/<int:stock_id>/', views.list_stock_item, name='list_stock_item'),
    path('delete/<int:stock_id>/', views.delete_stock_item, name='delete_stock_item'),
    path('category/add/', views.add_category, name='category_add'),
    path('category/delete/', views.delete_category, name='category_delete'),
]
