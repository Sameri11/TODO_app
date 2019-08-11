from django.shortcuts import render
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import User
from rest_framework.generics import CreateAPIView
from .serializers import UserSerializer, CreateTaskSerializer
from todos.models import Tasks


class CreateUserView(CreateAPIView):
    model = User
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer


class CreateTaskView(CreateAPIView):
    model = Tasks
    serializer_class = CreateTaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
# Create your views here.
