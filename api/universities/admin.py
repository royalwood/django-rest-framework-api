from django.contrib import admin

from .models import University, Campus, School, Course


admin.site.register(University)
admin.site.register(Campus)
admin.site.register(School)
admin.site.register(Course)
