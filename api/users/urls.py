from django.conf.urls import url

from config.routers import SharedRouter
from .views import (
    UserViewSet, MeViewSet, UserProfileDetailViewSet, ConnectionViewSet,
    ResetPasswordViewSet)


router = SharedRouter()
router.register(r'users/details', UserProfileDetailViewSet, base_name='user_detail')
router.register(r'users/me', MeViewSet, base_name='me')
router.register(r'users', UserViewSet, base_name='users')
router.register(r'connections', ConnectionViewSet, base_name='connections')

urlpatterns = [
    url(r'^resetpassword', ResetPasswordViewSet.as_view(), name="password_reset"),
]
