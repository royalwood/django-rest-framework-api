from config.routers import SharedRouter
from .views import ItemViewSet


router = SharedRouter()
router.register(r'marketplace/items', ItemViewSet, base_name='marketplaceitems')
