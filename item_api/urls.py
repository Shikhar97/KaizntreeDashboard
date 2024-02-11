from django.urls import path
from . import views

urlpatterns = [
    path("items/", views.dashboardApi),
    path('items/<int:id>/', views.dashboardApi),
    path("categories/", views.categoryApi),
    path("categories/<int:id>/", views.categoryApi),
    path("tags/", views.tagApi),
    path("tags/<int:id>/", views.tagApi),

]
