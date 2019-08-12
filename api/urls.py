from django.urls import path, re_path
from .views import CreateUserView, CreateTaskView, UpdateTaskView
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView
)
urlpatterns = [
    path('register/', CreateUserView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('task/new/', CreateTaskView.as_view(), name='new_task'),
    path('task/updated/<int:pk>', UpdateTaskView.as_view(), name='update_task')
]