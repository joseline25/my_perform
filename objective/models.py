from django.db import models
from django.contrib.auth.models import User
from .models_additional.task import Task
from django.core.validators import MinValueValidator
from decimal import Decimal


priorities = [('Low', 'Low'), ('Intermediate',
                               'Intermediate'), ('High', 'High')]
complexities = [('Easy', 'Easy'), ('Hard', 'Hard')]
objective_types = [('Financial', 'Financial'),
                   ('Non-Financial', 'Non-Financial')]


# Create skills models
class Skill(models.Model):
    skill_id = models.AutoField(primary_key=True, null=False)
    skill_name = models.CharField(max_length=100, null=False)
    skill_description = models.TextField(max_length=100, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.skill_name


class Team(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(max_length=300, null=False)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    skills = models.ManyToManyField(
        Skill, related_name="skills", through="TeamSkill")

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Tool(models.Model):
    tool_id = models.AutoField(primary_key=True)
    tool_name = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(max_length=200, null=True, blank=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    teams = models.ManyToManyField(
        Team, related_name="tools", through="TeamTool")

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.tool_name


class TeamSkill(models.Model):
    skill_id = models.ForeignKey(Skill, on_delete=models.PROTECT)
    team = models.ForeignKey(Team, on_delete=models.PROTECT)
    updated_by = models.ForeignKey(
        User, on_delete=models.PROTECT)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.team.name} uses {self.skill_id.skill_name}"


class TeamTool(models.Model):
    tool_id = models.ForeignKey(Tool, on_delete=models.PROTECT)
    team = models.ForeignKey(Team, on_delete=models.PROTECT)
    updated_by = models.ForeignKey(
        User, on_delete=models.PROTECT)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.team.name}"


class Objective(models.Model):

    priorities = [('Low', 'Low'), ('Intermediate',
                                   'Intermediate'), ('High', 'High')]
    complexities = [('Easy', 'Easy'), ('Hard', 'Hard')]
    objective_types = [('Financial', 'Financial'),
                       ('Non-Financial', 'Non-Financial')]

    objective_id = models.AutoField(primary_key=True)
    objective_name = models.CharField(max_length=300, blank=True, null=True)
    assign_to = models.ManyToManyField(
        to=User, unique=False, related_name="objectives_assigned_to", blank=True, null=True)
    visible_to = models.ManyToManyField(
        User,  related_name="visible_objectives", blank=True, null=True)
    # created_by = models.ForeignKey(
    #     User, on_delete=models.PROTECT, related_name="objectives_created")
    associated_task = models.ManyToManyField(
        Task, related_name="objectives", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    evaluator = models.ForeignKey(
        User, related_name="evaluator", on_delete=models.CASCADE, blank=True, null=True)
    repeat_date = models.DateTimeField(null=True, blank=True)
    deadline = models.DateTimeField(null=True, blank=True)
    action_phrase = models.CharField(max_length=300, null=False, blank=True)
    number = models.IntegerField(null=False)
    units = models.CharField(max_length=10)
    start_date = models.DateTimeField(null=False)
    end_date = models.DateTimeField(null=False)
    priority = models.CharField(choices=priorities, max_length=100)
    complexity = models.CharField(choices=complexities, max_length=100)
    objective_type = models.CharField(choices=objective_types, max_length=100)
    skills = models.ManyToManyField(
        Skill, related_name='objectives_skill', through="ObjectiveSkill", blank=True, null=True)
    tools = models.ManyToManyField(
        Tool, related_name='objectives_tool', through="ObjectiveTool", blank=True, null=True)
    dog = models.ManyToManyField(
        "DefinitionOfGood", related_name="definition_of_good", blank=True, null=True)
    is_draft = models.BooleanField(default=False)
    repeat = models.BooleanField(default=False)
    

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.objective_name}"


# Create the Defination of Good Model

class DefinitionOfGood(models.Model):
    dog_id = models.AutoField(primary_key=True)
    dog_criteria = models.CharField(max_length=100)
    # objective_id = models.ForeignKey(Objective, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Dog'

    def __str__(self):
        return f"{self.dog_criteria}"


class ObjectiveSkill(models.Model):
    objective_skill_id = models.AutoField(primary_key=True)
    skill_id = models.ForeignKey(Skill, on_delete=models.CASCADE)
    skill_name = models.CharField(max_length=200, null=False)
    objective_id = models.ForeignKey(Objective, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.skill_id.skill_name}"


class ObjectiveTool(models.Model):
    objective_tool_id = models.AutoField(primary_key=True)
    tool_id = models.ForeignKey(Tool, on_delete=models.CASCADE)
    tool_name = models.CharField(max_length=200, null=False)
    objective_id = models.ForeignKey(Objective, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.tool_id.tool_name}"

# for save as draft ( I have to change this.
# put all the fields of an objective instead of creating a foreign key)


class ObjectiveDraft(models.Model):
    objective = models.ForeignKey(Objective, on_delete=models.CASCADE)
    is_draft = models.BooleanField(default=True)

    def __str__(self):
        return self.objective.name


# KPI model
"""  
The syntax of a model is number - unit - frequency 
We measure an objectives with the KPIs associated to the objective.
 
"""


class KPI(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(null=False, blank=False)
    number = models.DecimalField(max_digits=10, decimal_places=1, null=False, blank=False, validators=[
                                 MinValueValidator(Decimal('0.01'), "Amount must be a positive interger")])
    frequency = models.CharField(max_length=50, blank=False, null=True)
    unit = models.CharField(max_length=50, blank=False, null=False)
    frequency = models.CharField(max_length=250, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    # the associated objectives
    objective = models.ForeignKey(
        Objective, blank=True, null=True, related_name="objective_kpis", on_delete=models.CASCADE)
    

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


#
