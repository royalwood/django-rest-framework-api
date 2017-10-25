from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """Any authenticated user can see and update their calendar, but only their
    own. Can not delete their calendar."""
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
