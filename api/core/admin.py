from django.contrib import admin

from .models import AppVersion, Category


admin.site.register(AppVersion)
admin.site.register(Category)
