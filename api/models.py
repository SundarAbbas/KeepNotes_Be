from django.db import models
from django.contrib.auth.models import User

class Priority(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
    
    
class Status(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
    

class Task(models.Model):
    title = models.CharField(max_length=200)    
    priority = models.ForeignKey(Priority , on_delete=models.CASCADE)
    status = models.ForeignKey(Status , on_delete=models.CASCADE)
    description = models.CharField(max_length=1000)
    date = models.DateField()
    user = models.ForeignKey(User,on_delete=models.CASCADE ,  default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Tasks"

    def __str__(self):
        return self.title

    def get_status_name(self):
        return self.status.name if self.status else "No Status"
        
    def get_priority_name(self):
        return self.priority.name if self.priority else "No Priority"
        
    

         