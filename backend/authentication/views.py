from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import RegisterSerializer, UpdateUserSerializer
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                return Response({
                    'user': serializer.data,
                    'message': 'User created successfully',
                }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        content = {'message': 'Você está autenticado!'}
        return Response(content)


class HasRoleView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, role):
        user = request.user
        if user.has_role(role):
            message = f"User {user.username} has the role {role}."
            return Response({"message": message})
        else:
            message = f"User {user.username} does not have the role {role}."
            return Response({"message": message}, status=403)

class HasPermissionView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, permission):
        user = request.user
        role = Role.objects.filter(user=user).first()
        if role:
            if role.permissions.filter(codename=permission).exists():
                return Response({'has_permission': True})
        return Response({'has_permission': False})

class UpdateUserView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UpdateUserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        refresh_token = request.data.get('refresh_token')
        token = RefreshToken(refresh_token)
        token.blacklist()

        return Response(status=status.HTTP_205_RESET_CONTENT)