from rest_framework.permissions import  BasePermission, SAFE_METHODS


class IsGroupAdminOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        """Any authenticated user can read, but only group admins can edit."""
        # Anyone can read
        if request.method in SAFE_METHODS:
            return True
        # Otherwise, only admins can modify a group
        return obj.user == request.user or obj.is_admin(request.user)


class IsEventOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user


class IsEventOwnerOrAttendeeOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Anyone can read
        if request.method in SAFE_METHODS:
            return True
        # Event owner can crud attendees
        if obj.event.owner == request.user:
            return True
        # Otherwise, only attendees can modify their attendance
        return obj.user == request.user
