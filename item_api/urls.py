from django.urls import path
from . import views

urlpatterns = [
    path("list/", views.list_stock_item),
    path("add/", views.add_stock_item),
    path("delete/", views.delete_stock_item),
    path('list/<int:stock_id>/', views.list_stock_item),
    path('delete/<int:stock_id>/', views.delete_stock_item),

    # path("categories/", views.list_category),
    # path("categories/<int:id>/", views.list_category),

]
