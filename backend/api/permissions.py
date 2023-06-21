from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """Проверка является ли пользователь администратором"""

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                if not request.user.is_authenticated
                else request.user.is_superuser
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                if not request.user.is_authenticated
                else request.user.is_superuser
                or request.user.is_authenticated)


class IsAuthorOrAdmin(permissions.BasePermission):
    """Проверка является ли пользователь администратором или автором"""

    def has_object_permission(self, request, view, obj):
        return (True if request.user.is_authenticated
                and request.user.is_superuser or obj.author == request.user
                or request.method == 'POST'
                else request.method in permissions.SAFE_METHODS)
