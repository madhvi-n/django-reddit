from django.urls import path, include
from .router import router, group_router

urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('api/v1/', include(group_router.urls)),
]
