from django.db import models
from django.contrib.auth.models import User 
from objective.models import Objective, Tool,Skill
from action.models_additionals.question import Question


class Actions(models.Model):
    action_id = models.AutoField(primary_key=True)
    objective = models.ForeignKey(Objective, on_delete=models.PROTECT)
    questions_id = models.ForeignKey(Question, on_delete=models.PROTECT)
    completion_time = models.TimeField(null=False)
    collaborators = models.ManyToManyField(User,related_name="actions", through="User" ,on_delete=models.PROTECT)
    comment = models.TextField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(User, on_delete=models.PROTECT)
    

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.objective.objective_name} related to {self.action_id}"




class ActionTool(models.Model):
    tool_id = models.ForeignKey(Tool, on_delete=models.CASCADE)
    related_action = models.ForeignKey(Actions, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    
    def __str__(self):
        return 
    
    
class ActionSkill(models.Model):
# <<<<<<< HEAD
#     skill_id = models.ForeignKey(Skill, on_delete=models.PROTECT)
#     # action_id = models.ForeignKey(Actions, on_delete=models.SET_NULL)
#     action_id = models.CharField(max_length=100)
    skill_id = models.ForeignKey(Skill,on_delete=models.PROTECT)
    action_id = models.ForeignKey(Actions,on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT) 



class Achievement(models.Model):
    achieve_id = models.AutoField(primary_key=True)
    achievement_name = models.CharField(max_length=200)
    description = models.TextField(max_length=200, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)

    class Meta:
        ordering=['-date_added']

    def __str__(self):
        return self.achievement_name

class ActionAchievement(models.Model):
    achievement_id = models.ForeignKey(Achievement, on_delete=models.PROTECT)
    action_id = models.ForeignKey(Actions, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(User, on_delete=models.PROTECT)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.achievement_id.achievement_name
       


