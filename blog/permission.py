from rest_framework import permissions

from .models import Post


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        # if isinstance(obj, Post):
        return obj.author == request.user or request.user.is_staff
