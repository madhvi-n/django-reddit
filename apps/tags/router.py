from rest_framework_nested import routers
from tags.views import TagViewSet

router = routers.SimpleRouter()

router.register(r"tags", TagViewSet)
