from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'ADMIN'
    
class IsTrainerOrAdmin(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['GYM_TRAINER', 'ADMIN']
    
class IsSelfOrAdmin(BasePermission):
    
    def has_permission(self, request, view):
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        
        if request.user.role == 'ADMIN':
            return True
        
        if hasattr(obj, 'user'):
            return obj.user == request.user
        
        return False