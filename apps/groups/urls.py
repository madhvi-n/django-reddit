from django.urls import include, path

from .router import group_router, router

urlpatterns = [
    path("api/v1/", include(router.urls)),
    path("api/v1/", include(group_router.urls)),
]
