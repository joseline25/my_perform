from django.db import models
from django.contrib.auth.models import User
from .models_additional.task import Task
from django.core.validators import MinValueValidator
from decimal import Decimal

# to enable assign_to field to point to User or team
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType


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
        User, on_delete=models.CASCADE, related_name='team_created')
    updated_at = models.DateTimeField(auto_now=True)
    skills = models.ManyToManyField(
        Skill, related_name="skills", through="TeamSkill")
    users = models.ManyToManyField(User, through='UserTeam')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class UserTeam(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey('Team', on_delete=models.CASCADE)


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
    repeat_frequency = [('Daily', 'Daily'), ('Weekly',
                                             'Weekly'), ('Monthly', 'Monthly')]

    objective_id = models.AutoField(primary_key=True)
    objective_name = models.CharField(max_length=300, blank=True, null=True)
    assign_to = models.ManyToManyField(
        to=User, unique=False, related_name="objectives_assigned_to", blank=True)
    visible_to = models.ManyToManyField(
        User,  related_name="visible_objectives", blank=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="objectives_created", default=1,)
    associated_task = models.ManyToManyField(
        Task, related_name="objectives", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    evaluator = models.ForeignKey(
        User, related_name="evaluator", on_delete=models.CASCADE, blank=True, null=True)
    repeat_date = models.CharField(
        choices=repeat_frequency, max_length=100, blank=True, null=True)
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
        Skill, related_name='objectives_skill', blank=True)
    tools = models.ManyToManyField(
        Tool, related_name='objectives_tool', blank=True)
    dog = models.TextField()
    is_draft = models.BooleanField(default=False)
    repeat = models.BooleanField(default=False)
    
    # test assign_to a team or user
    
    # use GenericForeignKey to allow assignment to either User or Team
    assign_to_to_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    assign_to_to_id = models.PositiveIntegerField(null=True, blank=True)
    assign_to_to = GenericForeignKey('assign_to_to_type', 'assign_to_to_id')
    
    # GenericRelation to store reverse relations
    assign_to_to_objectives = GenericRelation('Objective', related_query_name='assign_to_to_objectives')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.objective_name}"

    # override the save method
    def save(self, *args, **kwargs):
        # check if end_date is further than deadline
        if self.deadline and self.end_date and self.deadline < self.end_date:
            # set the end_date to the deadline
            self.end_date = self.deadline

        # check that repeat == True before setting repeat date
        if self.repeat == False:
            self.repeat_date = None
            
        # management de assign_to avec User and Team
        # set assign_to_totype based on the instance type
        if isinstance(self.assign_to_to, User):
            self.assign_to_to_type = ContentType.objects.get_for_model(User)
        elif isinstance(self.assign_to_to, Team):
            self.assign_to_to_type = ContentType.objects.get_for_model(Team)
        # on renvoit la main à la méthode save originale
        super().save(*args, **kwargs)


# Create the Definition of Good Model

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
    objective_id = models.ForeignKey(Objective, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.skill_id.skill_name}"


class ObjectiveTool(models.Model):
    objective_tool_id = models.AutoField(primary_key=True)
    tool_id = models.ForeignKey(Tool, on_delete=models.CASCADE)
    objective_id = models.ForeignKey(Objective, on_delete=models.CASCADE)

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


{
    "objective_name": "Test Objective",
    "assign_to": [1, 2],
    "visible_to": [1],
    "associated_task": [1],
    "evaluator": 1,
    "repeat_date": "Weekly",
    "deadline": "2024-02-01T12:00:00Z",
    "action_phrase": "Test Action",
    "number": 5,
    "units": "Test Units",
    "start_date": "2024-01-01T08:00:00Z",
    "end_date": "2024-01-31T18:00:00Z",
    "priority": "High",
    "complexity": "Hard",
    "objective_type": "Financial",
    "skills": [1, 2],
    "tools": [3],
    "dog": "the thing is working",
    "is_draft": False,
    "repeat": True
}
