from rest_framework import serializers

from .models import FileUpload


class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileUpload
        fields = ('user', 'object_id', 'filename', 'file_size')
        read_only_fields = ('user',)
