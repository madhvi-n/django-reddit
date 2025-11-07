from groups.views import (
    GroupInviteViewSet,
    GroupMemberViewSet,
    GroupRuleViewSet,
    GroupViewSet,
    MemberRequestViewSet,
)
from rest_framework_nested import routers

router = routers.SimpleRouter()
router.register(r"groups", GroupViewSet)
router.register(r"members", GroupMemberViewSet)

group_router = routers.NestedSimpleRouter(router, r"groups", lookup="group")
group_router.register(r"members", GroupMemberViewSet)
group_router.register(r"member_requests", MemberRequestViewSet)
group_router.register(r"invites", GroupInviteViewSet)
group_router.register(r"rules", GroupRuleViewSet)
