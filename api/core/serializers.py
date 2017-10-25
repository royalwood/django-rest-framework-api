from rest_framework import serializers

from .models import AppVersion, Category


class AppVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppVersion
        fields = ('dev', 'stg', 'prd', 'iphone_version', 'android_version')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'module', 'active')
