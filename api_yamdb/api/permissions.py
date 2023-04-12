from django.contrib.auth import get_user_model
from rest_framework.permissions import SAFE_METHODS, BasePermission


User = get_user_model()


class IsAdminUserOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        else:
            return request.user.is_staff


class IsUserRole(BasePermission):
    "Права доступа для роли User"
    allowed_roles = ['user']

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.role in self.allowed_user_roles:
                return True
        return False


class IsModeratorRole(BasePermission):
    "Права доступа для роли Moderator"
    allowed_roles = ['moderator']

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.role in self.allowed_user_roles:
                return True
        return False


class IsAdminRole(BasePermission):
    "Права доступа для роли Admin"
    allowed_roles = ['admin']

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.role in self.allowed_user_roles:
                return True
        return False


class IsObjectOwner(BasePermission):
    "Проверка прав к объекту для владельца"
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return obj.author == request.user
        return False
