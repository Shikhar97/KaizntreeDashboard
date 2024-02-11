"""
URL configuration for kaizntree_dashboard project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include
from rest_framework.schemas import get_schema_view
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('auth_api.urls')),
    path('items/', include('item_api.urls')),
    path('api_docs/',
         TemplateView.as_view(template_name='api_doc.html', extra_context={'schema_url': 'api_schema'}),
         name='swagger-ui'),
    path('api_schema/', get_schema_view(title='Kaizntree APIs', description='API documentation'),
         name='api-schema'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)