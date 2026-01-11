from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """Allows read-only access for anonymous users and full access for admin users."""

    def has_permission(self, request, view):
        # SAFE_METHODS are GET, HEAD, OPTIONS
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write operations (POST, PUT, PATCH, DELETE), require admin
        return request.user and request.user.is_staff
