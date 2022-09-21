from django.urls import include, path

from tags.router import router

urlpatterns = [
    path('api/v2/', include(router.urls)),
]
