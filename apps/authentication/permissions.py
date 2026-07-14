from rest_framework.permissions import BasePermission

class IsAdminUserRole(BasePermission):
    """allow access ony to users with the admin role."""
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role ==  'ADMIN'

class IsManagerUserRole(BasePermission):
    """allow access only to MANAGER /ADMIN"""
    def has_permission(self, request ,view):
        return request.user and request.user.is_authenticated and request.user.role in ['MANAGER', 'ADMIN']
    
class IsClientUserRole (BasePermission):
    """allows access only to authenticated users with the Client"""
    def has_permission(self ,request, view):
        return request.user and request.user.is_authenticated and request.user.role =='CLIENT'
    