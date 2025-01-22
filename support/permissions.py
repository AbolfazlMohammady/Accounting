from rest_framework.permissions import BasePermission

from .models import Ticket

class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Ticket):
            return obj.user == request.user or request.user.is_staff
        return False


class IsSupporterOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Ticket):
            return request.user.is_staff and (obj.supporter is None or obj.supporter == request.user)
        return False