from django.shortcuts import render
from rest_framework import permissions
from django.contrib.auth.models import User
from rest_framework.generics import CreateAPIView
from .serializers import UserSerializer


class CreateUserView(CreateAPIView):
    model = User
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer

# Create your views here.
