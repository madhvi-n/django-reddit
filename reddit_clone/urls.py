"""reddit_clone URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions


schema_view = get_schema_view(
    openapi.Info(
        title="Django Reddit API",
        default_version="v1",
        description="API documentation for the reddit clone project",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    # path('accounts/', include('allauth.urls')),
    re_path(r'^dj-rest-auth/', include('dj_rest_auth.urls')),
    re_path(r'^dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    path('', include('posts.urls')),
    path('', include('tags.urls')),
    path('', include('groups.urls')),
    path('', include('profiles.urls')),
    path('', include('reports.urls')),
        path(
        "api/swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="swagger-docs",
    ),
    path(
        "api/redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="redoc-docs",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
