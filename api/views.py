from django.shortcuts import render, get_object_or_404
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import User
from rest_framework.generics import (CreateAPIView, UpdateAPIView, ListAPIView, 
                                     DestroyAPIView)
from .serializers import UserSerializer, TaskSerializer
from todos.models import Tasks


class CreateUserView(CreateAPIView):
    model = User
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer


class CreateTaskView(CreateAPIView):
    model = Tasks
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UpdateTaskView(UpdateAPIView):
    model = Tasks
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Tasks.objects.filter(pk=self.kwargs['pk'])

    def get_object(self, queryset=None):
        queryset = self.get_queryset()
        return get_object_or_404(queryset)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class TaskListView(ListAPIView):
    model = Tasks
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if not self.kwargs:
            return Tasks.objects.filter(user=self.request.user)
        elif self.kwargs['status'] and not self.kwargs['priority']:
            return Tasks.objects.filter(user=self.request.user,
                                        task_status=self.kwargs['status'])
        elif self.kwargs['priority'] and not self.kwargs['status']:
            return Tasks.objects.filter(user=self.request.user,
                                        task_priority=self.kwargs['priority'])
        elif self.kwargs['status'] and self.kwargs['priority']:
            return Tasks.objects.filter(user=self.request.user).filter(
                    task_status=self.kwargs['status'], 
                    task_priority=self.kwargs['priority'])


class AdminTaskListView(ListAPIView):
    model = Tasks
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        return Tasks.objects.all()


class DeleteTaskView(DestroyAPIView):
    model = Tasks
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Tasks.objects.filter(pk=self.kwargs['pk'])

    def get_object(self, queryset=None):
        queryset = self.get_queryset()
        return get_object_or_404(queryset)

