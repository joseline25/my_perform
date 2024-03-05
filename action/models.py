from django.db import models
from django.contrib.auth.models import User
from objective.models import Objective, Tool, Skill


class Action(models.Model):
    achievements_type = [("Work-Product", "Work-Product"), ("Deliverable",
                                                            "Deliverable"), ("Learning", "Learning"), ("Miscellaneous", "Miscellaneous")]
    action_name = models.CharField(max_length=300)
    objective = models.ForeignKey(Objective, on_delete=models.CASCADE)
    # decimal avec 2 decimal , max = 10, blank=False, null=False
    completion_time = models.IntegerField(null=False)
    # ca va venir du front end en heures pour etre converti en secondes, nous on doit convertir en heures pour envoyer au front end
    collaborators = models.ManyToManyField(
        User, related_name="collaborators_action", blank=True)
    comment = models.TextField(max_length=200, null=True, blank=True)
    tools = models.ManyToManyField(
        Tool, through="ActionTool", related_name="tool_actions")
    skills = models.ManyToManyField(
        Skill, through="ActionSkill", related_name="skill_actions")
    achievements = models.CharField(
        max_length=100, choices=achievements_type, default="Deliverable")
    created_at = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f" {self.action_name} for {self.objective.objective_name}"
    
    
# action entry following the main action entry sheet
""" 
date, name, What you did you do today, objective(foreignkey), duration, 
achievements(learnings, deliverable, work product, innovation, miscellaneous)
"""

class ActionMainEntry(models.Model):
    achievements_values = [
        ('Learnings', 'Learnings'),
        ('Deliverable', 'Deliverable'),
        ('Work-Product', 'Work-Product'),
        ('Innovation', 'Innovation'),
        ('Miscellaneous', 'Miscellaneous'),
    ]
    
    date= models.DateTimeField(auto_now=True)
    name = models.ForeignKey(User, related_name="action_main_entry_user", on_delete=models.SET_NULL, null=True)
    what_you_did_today = models.TextField()
    objective = models.ForeignKey(Objective, related_name='action_entry', on_delete=models.CASCADE)
    duration = models.IntegerField(null=True)
    achievements = models.CharField(choices=achievements_values, default='Learnings', max_length=20)
    collaborators = models.ManyToManyField(User, related_name="action_main_entry_collaborators")
    skills = models.ManyToManyField(Skill, related_name='action_main_entry_skills', blank=True)
    tools = models.ManyToManyField(Tool, related_name='action_main_entry_tools', blank=True)
    
    class Meta:
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.name.first_name}'s actions for {self.date}"
    


{
    "date": "2024-02-14T12:00:00Z",
    "name": 1,  
    "what_you_did_today": "Worked on project tasks.",
    "objective": 1,  
    "duration": 120,  
    "achievements": "Deliverable",
    "collaborators": [1, 2]  
}


class ActionTool(models.Model):
    tool_id = models.ForeignKey(Tool, on_delete=models.CASCADE)
    action_id = models.ForeignKey(Action, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.tool_id.tool_name


class ActionSkill(models.Model):
    skill_id = models.ForeignKey(Skill, on_delete=models.PROTECT)
    action_id = models.ForeignKey(Action, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.skill_id.skill_name} for {self.action_id.action_name}"


class Question(models.Model):
    question = models.TextField(null=True, blank=True)
    action = models.ForeignKey(
        Action, related_name='questions', on_delete=models.CASCADE)
    objective = models.ForeignKey(
        Objective, on_delete=models.CASCADE, null=True)
    number = models.IntegerField(null=True,)
    answer = models.BooleanField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question





{
    "action_name": "first action",
    "objective": 1,
    "completion_time": 3,
    "collaborators": [1, 2],
    "comment": "the first action to test the form of the model",
    "tools": [],
    "skills": [],
    "achievements": "Deliverable",
    "added_by": 1
}
