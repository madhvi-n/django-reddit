from django.urls import include, path, re_path
from reports.router import router

urlpatterns = [
    path("api/v1/", include(router.urls)),
]
