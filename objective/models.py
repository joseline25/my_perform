from django.db import models
from django.contrib.auth.models import User
from .models_additional.task import Task



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
    skill_id = models.ForeignKey(Skill, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    updated_by = models.ForeignKey(
        User, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']
        
    def __str__(self):
        return f"{self.team.name} uses {self.skill_id.skill_name}"


class TeamTool(models.Model):
    tool_id = models.ForeignKey(Tool, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    updated_by = models.ForeignKey(
        User, on_delete=models.CASCADE)
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
        to=User, unique=False, related_name="objectives_assigned_to")
    visible_to = models.ManyToManyField(
        User,  related_name="visible_objectives")
    # created_by = models.ForeignKey(
    #     User, on_delete=models.CASCADE, related_name="objectives_created")
    associated_task = models.ManyToManyField(
        Task, related_name="objectives")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    evaluator = models.ForeignKey(
        User, related_name="evaluator", on_delete=models.CASCADE)
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
        Skill, related_name='objectives_skill', through="ObjectiveSkill")
    tools = models.ManyToManyField(
        Tool, related_name='objectives_tool', through="ObjectiveTool")
    dog = models.ManyToManyField(
        "DefinitionOfGood", related_name="definition_of_good")
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
    #objective_id = models.ForeignKey(Objective, on_delete=models.CASCADE)
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
    
# for save as draft
class ObjectiveDraft(models.Model):
    objective = models.ForeignKey(Objective, on_delete=models.CASCADE)
    is_draft = models.BooleanField(default=True)
    
