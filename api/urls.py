from django.urls import path, re_path
from .views import (CreateUserView, CreateTaskView, UpdateTaskView,
                    TaskListView, AdminTaskListView, DeleteTaskView)
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView
)
urlpatterns = [
    path('register/', CreateUserView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('task/new/', CreateTaskView.as_view(), name='new_task'),
    path('task/updated/<int:pk>', UpdateTaskView.as_view(), name='update_task'),
    path('task/list/', TaskListView.as_view(), name='task_list'),
    path('task/list/filter/<int:status>/<int:priority>/', 
         TaskListView.as_view(), name='task_list_filtered'),
    path('task/list/admin/', AdminTaskListView.as_view(), 
         name='admin_task_list'),
    path('task/destroyed/<int:pk>/', DeleteTaskView.as_view(), 
         name='destroyed_task')
]