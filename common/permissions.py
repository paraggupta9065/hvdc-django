from rest_framework.permissions import BasePermission


class IsActiveUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_active


class IsSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.role == 'superadmin'
        return False


class IsEditor(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.role == 'editor'
        return False


class IsReader(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.role == 'reader'
        return False


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.role == 'admin'
        return False


class IsMember(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.role == 'member'
        return False


class IsAdminOrSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.role in ['admin', 'superadmin']
        return False


class IsAdminOrSuperAdminOrEditor(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.role in ['admin', 'superadmin', 'editor']
        return False
