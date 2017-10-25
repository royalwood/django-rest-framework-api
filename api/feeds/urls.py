from config.routers import SharedRouter
from feeds.views import (
    PostViewSet, CommentViewSet, PollAnswerViewSet, PostLogViewSet)


router = SharedRouter()
router.register(r'feeds/comments', CommentViewSet, base_name='postcomments')
router.register(r'feeds/postlog', PostLogViewSet, base_name='postlog')
router.register(r'feeds/pollanswers', PollAnswerViewSet, base_name='pollanswers')
router.register(r'feeds/posts', PostViewSet, base_name='posts')
