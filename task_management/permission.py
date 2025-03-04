from rest_framework import  permissions
from .models import Task

class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
         

class IsOwnerOrMembers(permissions.BasePermission):
    """
    فقط کاربری که صاحب پروژه است یا به او اختصاص داده شده، اجازه مشاهده دارد.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user or   request.user in obj.members.all()
    

class IsOwnerOrAssigned(permissions.BasePermission):
    """
    فقط کاربری که صاحب تسک است یا به او اختصاص داده شده، اجازه مشاهده دارد.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user or obj.assigned_user == request.user