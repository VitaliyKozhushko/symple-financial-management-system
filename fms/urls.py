"""
URL configuration for fms project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)
from django.contrib import admin
from django.urls import (path,
                         re_path,
                         include)
from django.conf import settings
from django.conf.urls.static import static

SchemaView = get_schema_view(
    openapi.Info(
        title="Symple financial management system API",
        default_version='v1',
        description="API documentation",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="itvkip@yandex.ru"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[AllowAny],
    authentication_classes=[],
)

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('login/', TokenObtainPairView.as_view(), name='get_token'),
                  path('users/', include('users.urls')),
                  path('transactions/', include('fin_transactions.urls_transactions')),
                  path('report/', include('fin_transactions.urls_reports')),
                  path('budgets/', include('budget.urls')),
                  path('token/refresh/', TokenRefreshView.as_view(), name='refresh_token'),
                  path('redoc/', SchemaView.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
                  path('swagger/', SchemaView.with_ui('swagger', cache_timeout=0),
                       name='schema-swagger-ui'),
                  re_path(r'^swagger(?P<format>\.json|\.yaml)$',
                          SchemaView.without_ui(cache_timeout=0), name='schema-json'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
