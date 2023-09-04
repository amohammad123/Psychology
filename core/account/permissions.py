from rest_framework import permissions


class ClientPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if obj.is_trappist:
            return False
        return obj.is_valid


class TrappistPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if not obj.is_valid:
            return False
        return obj.is_trappist
