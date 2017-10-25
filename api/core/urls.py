from config.routers import SharedRouter
from .views import AppVersionViewSet # , CategoryViewSet


router = SharedRouter()
router.register(r'mobile', AppVersionViewSet, base_name='mobile')
