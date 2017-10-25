"""Routers"""
from rest_framework.routers import SimpleRouter, DefaultRouter


class SharedRouter(SimpleRouter):
    """Used to share a DefaultRouter among the urls of all apps"""
    shared_router = DefaultRouter(trailing_slash=False)

    def register(self, *args, **kwargs):
        self.shared_router.register(*args, **kwargs)
        super().register(*args, **kwargs)
