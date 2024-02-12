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
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api/v1/auth/', include('auth_api.urls')),
    path('api/v1/items/', include('item_api.urls')),
    path('v1/api_docs/',
         TemplateView.as_view(template_name='api_doc.html', extra_context={'schema_url': 'api_schema'}),
         name='swagger-ui'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
