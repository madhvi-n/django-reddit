from django.urls import include, path

from .router import post_router, router

urlpatterns = [
    path("api/v1/", include(router.urls)),
    path("api/v1/", include(post_router.urls)),
]
