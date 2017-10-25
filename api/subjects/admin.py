from django.contrib import admin

from .models import Subject, SubjectTag, SubjectEnrollee


admin.site.register(Subject)
admin.site.register(SubjectTag)
admin.site.register(SubjectEnrollee)
