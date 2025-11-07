from followers.views import UserFollowerViewSet
from profiles.views import ProfileViewSet
from reports.views import UserProfileReportViewSet
from rest_framework_nested import routers

router = routers.SimpleRouter()
router.register(r"users", ProfileViewSet)
user_profile_router = routers.NestedSimpleRouter(router, r"users", lookup="user")
user_profile_router.register(r"reports", UserProfileReportViewSet)
user_profile_router.register(r"followers", UserFollowerViewSet)
