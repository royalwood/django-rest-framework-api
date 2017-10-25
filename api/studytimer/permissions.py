from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """Any authenticated user can add, change or delete their own study timer
    entry.
    """
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
