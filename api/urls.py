from django.urls import path, re_path
from .views import CreateUserView, AdminTaskListView, TasksViewSet
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView
)
urlpatterns = [
    path('register/', CreateUserView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('tasks/admin/', AdminTaskListView.as_view(),
         name='admin_task_list'),
]
router = routers.SimpleRouter()
router.register(r'tasks', TasksViewSet, basename='tasks')
urlpatterns += router.urls
