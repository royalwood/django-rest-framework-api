from rest_framework.permissions import (
    BasePermission, IsAuthenticated, SAFE_METHODS)


class IsPosterOrReadOnly(BasePermission):
    """Posters can edit their own post."""
    def has_object_permission(self, request, view, obj):
        # Anyone can read a post
        if request.method in SAFE_METHODS:
            return True
        # Only the owner can modify
        return obj.user == request.user


class IsAnswerer(BasePermission):
    """Any user can add, change or delete their own answer."""
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
