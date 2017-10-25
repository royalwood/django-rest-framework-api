from config.routers import SharedRouter
from .views import KeywordViewSet


router = SharedRouter()
router.register(r'keywords', KeywordViewSet, base_name='keywords')
