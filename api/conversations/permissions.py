from rest_framework.permissions import BasePermission, IsAuthenticated


class IsSenderOrReceiver(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Deny access to the record if the authenticated user is not the sender
        # of the message
        return obj.sender == request.user
