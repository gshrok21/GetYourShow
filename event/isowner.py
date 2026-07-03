from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allow GET (optional)
        if request.method in SAFE_METHODS and request.user.is_authenticated:
            return True   # only owner can even view

        # Allow PUT, PATCH, DELETE only for owner
        return obj.organizer == request.user
        

class myregistered(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allow GET (optional)
        if request.method in SAFE_METHODS and not request.user.is_authenticated:
            return obj.user == request.user
            # only owner can even view

        # Allow PUT, PATCH, DELETE only for owner
        return False