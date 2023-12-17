from rest_framework.permissions import BasePermission
from .roles import UserRoles


class IsClientUser(BasePermission):
    """
    Allows access only to client users.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == UserRoles.CLIENT)
