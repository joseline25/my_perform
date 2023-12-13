from django.db import models
from objective.models import Objective, Tool
from django.contrib.auth.models import User

# Create your models here.
class Question(models.Model):
    question = models.TextField(null=True, blank=True)
    number = models.IntegerField(null=True,)
    answer = models.BooleanField(null=True)
    related_action = models.ForeignKey(Action, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.question
    
    
class ActionTool(models.Model):
    tool_id = models.ForeignKey(Tool, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL)
    
    def __str__(self):
        return 
    
    
class ActionSkill(models.Model):
    skill_id = models.ForeignKey()
    action_id = models.ForeignKey(Action, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)        


class Collaborator(models.Model):
    collaborator_id = models.ForeignKey(User, on_delete=models.CASCADE)    
    created_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)