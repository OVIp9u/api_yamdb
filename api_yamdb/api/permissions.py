from django.contrib.auth import get_user_model
from rest_framework.permissions import SAFE_METHODS, BasePermission

User = get_user_model()


class IsAdminUserOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_staff
        )


class IsUserRole(BasePermission):
    """Права доступа для роли User"""

    def has_permission(self, request, view):
        return request.user.is_authenticated


class IsModeratorRole(BasePermission):
    """Права доступа для роли Moderator"""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_moderator_role

class IsAdminRole(BasePermission):
    """Права доступа для роли Admin"""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin_role


class ObjectPermissions(BasePermission):
    "Проверка прав к объекту для владельца"

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.user.is_admin_role
            or request.user.is_moderator_role
            or obj.author == request.user
        )
