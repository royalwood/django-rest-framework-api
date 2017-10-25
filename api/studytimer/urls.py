from config.routers import SharedRouter
from .views import EntryViewSet


router = SharedRouter()
router.register(r'studytimer', EntryViewSet, base_name='studytimer')
