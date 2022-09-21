from rest_framework_nested import routers
from profiles.views import ProfileViewSet


router = routers.SimpleRouter()
router.register(r'users', ProfileViewSet)
