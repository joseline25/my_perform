from django.db import models
from django.contrib.auth.models import User
from objective.models import Objective, Tool, Skill
from .models_additionals.question import Question
from objective.models import Tool, Skill


class Action(models.Model):
    action_name = models.CharField(max_length=300)
    objective = models.ForeignKey(Objective, on_delete=models.PROTECT)
    questions = models.ForeignKey(
        Question, on_delete=models.PROTECT, related_name="related_actions")
    completion_time = models.IntegerField(null=False)
    collaborators = models.ManyToManyField(
        User, related_name="actions", blank=True)
    comment = models.TextField(max_length=200, null=True, blank=True)
    tools = models.ManyToManyField(
        Tool, through="ActionTool", related_name="tool_actions")
    skills = models.ManyToManyField(
        Skill, through="ActionSkill", related_name="skill_actions")
    achievements = models.ManyToManyField(
        "Achievement", through="ActionAchievement", related_name="achievement_actions")
    created_at = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(User, on_delete=models.PROTECT)

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


class Achievement(models.Model):
    achievement_name = models.CharField(max_length=200)
    description = models.TextField(max_length=200, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)

    class Meta:
        ordering = ['-date_added']

    def __str__(self):
        return self.achievement_name


class ActionAchievement(models.Model):
    achievement_id = models.ForeignKey(Achievement, on_delete=models.PROTECT)
    action_id = models.ForeignKey(Action, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(User, on_delete=models.PROTECT)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.achievement_id.achievement_name} for {self.action_id.action_name} "
