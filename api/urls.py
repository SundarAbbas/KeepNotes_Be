from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import TaskViewSet, StatusViewSet, PriorityViewSet 
from api.views import BreakTaskView , UserPrompt

router = DefaultRouter()

router.register(r'tasks', TaskViewSet, basename='task') 
router.register(r'statuses', StatusViewSet)
router.register(r'priorities', PriorityViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('ai/break-task/', BreakTaskView.as_view(), name='break-task'),
    path('ai/user-prompt/', UserPrompt.as_view(), name='user-prompt'),
]