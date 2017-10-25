"""Global urlconf"""
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.views.static import serve

from config.routers import SharedRouter
from config.auth import CustomTokenView

#pylint:disable=unused-import
import conversations.urls as _
import core.urls as _
import feeds.urls as _
import groups.urls as _
import keywords.urls as _
import marketplace.urls as _
import notifications.urls as _
import studentcalendar.urls as _
import studytimer.urls as _
import subjects.urls as _
import universities.urls as _
import users.urls as _


# Move this into uploads app
from upload_file.views import FileUploadView

urlpatterns = [
    url(r'^', include(SharedRouter.shared_router.urls, namespace='api')),
    url(r'^api-auth', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-docs/', include('rest_framework_docs.urls')),
    url(r'^oauth/token/$', CustomTokenView.as_view(), name='token'), # Our custom token view which includes the user object
    url(r'^oauth/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^ucroo-admin-382/', include(admin.site.urls)),
    url(r'^groups', include('groups.urls')),
    url(r'^activity', include('activity.urls')),
    url(r'^search', include('search.urls')),
    url(r'^happening', include('happening.urls')),
    url(r'^users', include('users.urls')),

    # Move these into uploads app!
    url(r'^uploads', FileUploadView.as_view()),
    url(r'^uploads/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
