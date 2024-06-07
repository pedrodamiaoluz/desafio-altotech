from rest_framework.permissions import BasePermission


class EhOProprioUsuario(BasePermission):
    message = "Restrito ao proprio usuário"

    def has_object_permission(self, request, view, obj):
        return request.user and request.user == obj
