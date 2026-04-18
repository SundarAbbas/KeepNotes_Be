from rest_framework import serializers
from api.models import Task , Status , Priority  
from django.contrib.auth.models import User
 

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'
        
        
class PrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = Priority
        fields = '__all__'
        
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'                 
        
    
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
