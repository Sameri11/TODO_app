from django.urls import path, re_path
from .views import (CreateUserView, CreateTaskView, UpdateTaskView,
                    TaskListView, AdminTaskListView, DeleteTaskView,
                    TasksViewSet)
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView
)
urlpatterns = [
    path('register/', CreateUserView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('tasks/new/', CreateTaskView.as_view(), name='new_task'),
    path('tasks/updated/<int:pk>', UpdateTaskView.as_view(), name='update_task'),
    path('tasks/list/', TaskListView.as_view(), name='task_list'),
    path('tasks/list/filter/<int:status>/<int:priority>/', 
         TaskListView.as_view(), name='task_list_filtered'),
    path('tasks/list/admin/', AdminTaskListView.as_view(), 
         name='admin_task_list'),
    path('tasks/destroyed/<int:pk>/', DeleteTaskView.as_view(), 
         name='destroyed_task')
]
router = routers.SimpleRouter()
router.register(r'task', TasksViewSet, basename='tasks')
urlpatterns += router.urls