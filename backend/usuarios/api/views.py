from django.contrib.auth import login, logout
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.decorators import action

from usuarios.api.serializers import (
    LoginSerializer,
    UserChangeSerializer,
    UserSerializer,
    ChangePasswordSerializer,
)
from usuarios.models import CustomUser


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()

    def get_permissions(self):
        permission_classes = []
                    
        if self.action in ["list"]:
            permission_classes.append(IsAdminUser)

        if self.action in ['create']:
            permission_classes.append(AllowAny)
        else:
            permission_classes.append(IsAuthenticated)
        return [permission() for permission in self.permission_classes]

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update', 'destroy', 'retrieve']:
            return UserChangeSerializer
        if self.action == "set_password":
            return ChangePasswordSerializer
        return UserSerializer  # actions = 'list', 'create'

    @action(detail=True, methods=['POST'], name="Mudar senha")
    def set_password(self, request, pk=None):
        serializer_class = self.get_serializer_class()
        user = self.get_object()
        serializer = serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user.set_password(serializer.validated_data["password"])
        user.save()
        return Response({"sucesso": "Nova senha definida"},
                        status=status.HTTP_200_OK)


class LoginAPIView(APIView):
    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.usuario_ehAutenticado()
        login(request, user)
        return Response(data={'usuário logado': user.email},
                        status=status.HTTP_200_OK)


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        email = request.user.email
        logout(request)
        return Response(data={'usuário deslogado': email},
                        status=status.HTTP_200_OK)
