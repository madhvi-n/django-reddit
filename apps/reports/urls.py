from django.urls import re_path, path, include
from reports.router import router

urlpatterns = [
    path('api/v1/', include(router.urls)),
]
