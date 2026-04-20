from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from api.models import Task ,  Priority ,  Status
from api.serializers import TaskSerializer , PrioritySerializer , StatusSerializer , SignupSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import action

class StatusViewSet(ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    
class PriorityViewSet(ModelViewSet):
    queryset = Priority.objects.all()
    serializer_class = PrioritySerializer    
    
class TaskViewSet(ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    
    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        task = self.get_object()
        status_id = request.data.get('status_id')
        try:
            new_status = Status.objects.get(id=status_id)
            task.status = new_status
            task.save()
            serializer = self.get_serializer(task)
            return Response(serializer.data)
        except Status.DoesNotExist:
            return Response({'error': 'Status not found'}, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)    
    
class SignUpView(generics.CreateAPIView):
    queryset =  User.objects.all()   
    serializer_class = SignupSerializer
    