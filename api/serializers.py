from rest_framework import serializers
from api.models import Task , Status , Priority  
from django.contrib.auth.models import User
 

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ['id','name']
        
class PrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = Priority
        fields = ['id','name']
        
class TaskSerializer(serializers.ModelSerializer):
    status_name = serializers.CharField(source='status.name', read_only=True)
    priority_name = serializers.CharField(source='priority.name', read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'date', 'status', 'priority', 
                  'status_name', 'priority_name', 'user', 'created_at']
        read_only_fields = ['user', 'created_at']         
        
    
class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)            
    
    class Meta:
        model = User
        fields = ('id', 'username','email','password')
    
    def create(self , validated_data):
        user = User.objects.create_user(
            username = validated_data['username'],            
            email = validated_data.get('email',''),            
            password = validated_data['password'],            
        )    
        return user
