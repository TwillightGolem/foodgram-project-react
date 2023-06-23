from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """Проверка является ли пользователь администратором"""

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_superuser)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_superuser)


class IsAuthorOrAdmin(permissions.BasePermission):
    """Проверка является ли пользователь администратором или автором"""

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_superuser or obj.author == request.user)
