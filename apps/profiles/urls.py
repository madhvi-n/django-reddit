from django.urls import include, path, re_path
from profiles.views import IsAuthenticatedView

from .router import router

urlpatterns = [
    path("api/v1/", include(router.urls)),
    re_path(
        r"^api/v1/is_authenticated/$",
        IsAuthenticatedView.as_view(),
        name="is_authenticated",
    ),
]
