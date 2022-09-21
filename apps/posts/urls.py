from django.urls import path, include
from .router import router, post_router

urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('api/v1/', include(post_router.urls))
]
