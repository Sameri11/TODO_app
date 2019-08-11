from django.urls import path
from .views import CreateUserView, CreateTaskView
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView
)
urlpatterns = [
    path('register/', CreateUserView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('new_task/', CreateTaskView.as_view(), name='new_task')
]