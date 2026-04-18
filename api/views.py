from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from api.models import Task ,  Priority ,  Status
from api.serializers import TaskSerializer , PrioritySerializer , StatusSerializer , SignupSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from django.contrib.auth.models import User

class StatusViewSet(ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    
class PriorityViewSet(ModelViewSet):
    queryset = Priority.objects.all()
    serializer_class = PrioritySerializer    
    
class TaskViewSet(ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)    
    
class SignUpView(generics.CreateAPIView):
    queryset =  User.objects.all()   
    serializer_class = SignupSerializer
    