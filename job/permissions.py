from rest_framework import permissions
from users.models import *


class IsGroupMember(permissions.BasePermission):
    """
    this permission class is used to check if user is member of Companies Group
    """

    def has_permission(self, request, view):
        group_name = "Companies Group"
        if request.user.groups.filter(name=group_name).exists():
            return True
        return False


class IsEmployee(permissions.BasePermission):
    """
    this permission class is used to check if user is member of Employee Group
    """

    def has_permission(self, request, view):
        group_name = "Employee Group"
        if request.user.groups.filter(name=group_name).exists():
            return True
        return False
