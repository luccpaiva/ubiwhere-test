from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission class:
    - Anonymous users can only read (GET, HEAD, OPTIONS)
    - Admin users (is_staff=True) can perform all operations
    """

    def has_permission(self, request, view):
        # SAFE_METHODS are GET, HEAD, OPTIONS
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write operations (POST, PUT, PATCH, DELETE), require admin
        return request.user and request.user.is_staff
