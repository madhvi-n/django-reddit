from bookmarks.views import PostBookmarkViewSet
from comments.views import PostCommentViewSet
from followers.views import PostFollowerViewSet
from posts.views import PostSelfViewSet, PostViewSet
from reports.views import PostReportViewSet
from rest_framework_nested import routers

router = routers.SimpleRouter()
router.register(r"posts", PostViewSet)
router.register(r"post/self", PostSelfViewSet, basename="post-self")

post_router = routers.NestedSimpleRouter(router, r"posts", lookup="post")
post_router.register(r"comments", PostCommentViewSet)
post_router.register(r"bookmarks", PostBookmarkViewSet)
post_router.register(r"reports", PostReportViewSet)
post_router.register(r"followers", PostFollowerViewSet)
