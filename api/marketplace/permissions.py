from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsSellerOrReadOnly(BasePermission):
    """Authenticated user can add/change/delete their own for-sale item."""
    def has_object_permission(self, request, view, obj):
        # Anyone can read
        if request.method in SAFE_METHODS:
            return True
        # Seller can write
        return obj.user == request.user
