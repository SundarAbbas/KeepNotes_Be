from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import TaskViewSet, StatusViewSet, PriorityViewSet

router = DefaultRouter()

router.register(r'tasks', TaskViewSet, basename='task') 
router.register(r'statuses', StatusViewSet)
router.register(r'priorities', PriorityViewSet)

urlpatterns = [
    path('', include(router.urls)),
]