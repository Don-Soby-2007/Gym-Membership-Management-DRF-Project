from rest_framework.permissions import BasePermission


class IsTrainer(BasePermission):

    def has_permission(self, request, view):
        return request.user.role == 'GYM_TRAINER'
    
class IsOwner(BasePermission):

    def has_permission(self, request, view):
        return request.user.role == 'ADMIN'