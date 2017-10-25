from django.conf.urls import url

from .views import HappeningView


urlpatterns = [
    url(r'$', HappeningView.as_view()),
]
