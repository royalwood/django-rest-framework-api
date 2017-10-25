"""Activity urls"""
from django.conf.urls import url

from .views import ActivityView


urlpatterns = [
    url(r'$', ActivityView.as_view(), name='activity'),
]
