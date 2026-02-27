from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS: # GET, HEAD, OPTIONS
            return True
        # Өзгерту немесе өшіру үшін: нысанның авторы request.user болуы керек
        # User моделі үшін obj өзі болуы керек, басқалар үшін obj.author
        return getattr(obj, 'author', obj) == request.user