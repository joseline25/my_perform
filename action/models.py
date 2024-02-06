from django.db import models
from django.contrib.auth.models import User
from objective.models import Objective, Tool, Skill
from objective.models import Tool, Skill


class Action(models.Model):
    achievements_type = [("Work-Product", "Work-Product"), ("Deliverable",
                                                            "Deliverable"), ("Learning", "Learning"), ("Miscellaneous", "Miscellaneous")]
    action_name = models.CharField(max_length=300)
    objective = models.ForeignKey(Objective, on_delete=models.CASCADE)
    # decimal avec 2 decimal , max = 10, blank=False, null=False
    completion_time = models.IntegerField(null=False)
    # ca va venir du front end en heures pour etre converti en secondes, nous on doit convertir en heures pour envoyer au front end
    collaborators = models.ManyToManyField(User, related_name="collaborators_action", blank=True)
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
