from posts.views import PostViewSet, PostSelfViewSet
from rest_framework_nested import routers
from bookmarks.views import PostBookmarkViewSet
from comments.views import PostCommentViewSet
from followers.views import PostFollowerViewSet

router = routers.SimpleRouter()
router.register(r'posts', PostViewSet)
router.register(r'post/self', PostSelfViewSet)

post_router = routers.NestedSimpleRouter(
    router, r'posts', lookup='post'
)
post_router.register(r'comments', PostCommentViewSet)

post_router.register(r'bookmarks', PostBookmarkViewSet)
post_router.register(r'followers', PostFollowerViewSet)
