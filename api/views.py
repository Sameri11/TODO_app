from django.shortcuts import render, get_object_or_404
from rest_framework import permissions, viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User
from rest_framework.generics import (CreateAPIView, UpdateAPIView, ListAPIView, 
                                     DestroyAPIView)
from .serializers import UserSerializer, TaskSerializer
from todos.models import Tasks


class CreateUserView(CreateAPIView):
    model = User
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer


class AdminTaskListView(ListAPIView):
    model = Tasks
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        return Tasks.objects.all()


class TasksViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer

    def get_queryset(self):
        queryset = Tasks.objects.filter(user=self.request.user)
        status = self.request.query_params.get('status', None)
        priority = self.request.query_params.get('priority', None)
        if status is not None and priority is not None:
            queryset = queryset.filter(status=status).filter(
                       priority=priority)
        elif status is not None:
            queryset = queryset.filter(status=status)
        elif priority is not None:
            queryset = queryset.filter(priority=priority)

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
