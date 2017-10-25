from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsEnrolleeOrReadOnly(BasePermission):
    """Any authenticated user can see enrollees. Only enrollees can edit their
    enrollment in a subject."""
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user
