from django.contrib.auth import get_user_model
from rest_framework.permissions import SAFE_METHODS, BasePermission

User = get_user_model()


class IsAdminUserOrReadOnly(BasePermission):
    """Права доступа для безопасных запросов или роли Admin"""
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_staff
        )


class IsAdminRole(BasePermission):
    """Права доступа для роли Admin"""

    def has_permission(self, request, view):
        return (request.user.is_authenticated and request.user.is_admin_role)


class IsAdminIsModeratorIsAuthor(BasePermission):
    """Проверка прав на просмотр для анонимных пользователей.
    Права на изменения объекта доступны только Администратору,
    Модератору и автору объекта"""

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.user.is_staff
            or request.user.is_admin_role
            or request.user.is_moderator_role
            or obj.author == request.user
        )
