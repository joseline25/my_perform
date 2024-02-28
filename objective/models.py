from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from .models_additional.task import Task
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.core.exceptions import ValidationError

from django.utils import timezone

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
    skill_name = models.CharField(max_length=300, null=False)
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
    name = models.CharField(max_length=300)
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
    team = models.ForeignKey(Team, on_delete=models.CASCADE)


class Tool(models.Model):
    tool_id = models.AutoField(primary_key=True)
    tool_name = models.CharField(max_length=300, null=True, blank=True)
    description = models.TextField(max_length=300, null=True, blank=True)
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
    status_choices = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]

    objective_id = models.AutoField(primary_key=True)
    objective_name = models.CharField(max_length=300, blank=True, null=True)
    assign_to = models.ManyToManyField(
        to=User, unique=False, related_name="objectives_assigned_to", blank=True)
    visible_to = models.ManyToManyField(
        User,  related_name="visible_objectives", blank=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="objectives_created", default=1,)
    associated_task = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    evaluator = models.ForeignKey(
        User, related_name="evaluator", on_delete=models.CASCADE, blank=True, null=True)
    repeat_date = models.CharField(
        choices=repeat_frequency, max_length=300, blank=True, null=True)
    deadline = models.DateTimeField(null=True, blank=True)
    action_phrase = models.CharField(max_length=300, null=False, blank=True)
    number = models.IntegerField(null=False)
    units = models.CharField(max_length=300)
    start_date = models.DateTimeField(null=False)
    end_date = models.DateTimeField(null=False)
    priority = models.CharField(choices=priorities, max_length=300)
    complexity = models.CharField(choices=complexities, max_length=300)
    objective_type = models.CharField(choices=objective_types, max_length=300)
    skills = models.ManyToManyField(
        Skill, related_name='objectives_skill', blank=True)
    tools = models.ManyToManyField(
        Tool, related_name='objectives_tool', blank=True)
    dog = models.TextField()
    is_draft = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)
    repeat = models.BooleanField(default=False)
    status = models.CharField(choices=status_choices,
                              default='Pending', max_length=300)
    completion_date = models.DateTimeField(blank=True, null=True)
    """
    To have a completion_date, mark the status as Completed! 
    """
    estimated_hours = models.IntegerField(
        default=0, help_text="Estimated number of hours to complete the task")
    # an objective is related to an operational goal
    operational_goal = models.ForeignKey("OperationalGoal", on_delete=models.SET_NULL, blank=True, null=True, related_name='objectives'
    )
    # test assign_to a team or user

    # use GenericForeignKey to allow assignment to either User or Team
    assign_to_to_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, null=True, blank=True)
    assign_to_to_id = models.PositiveIntegerField(null=True, blank=True)
    assign_to_to = GenericForeignKey('assign_to_to_type', 'assign_to_to_id')

    # GenericRelation to store reverse relations
    assign_to_to_objectives = GenericRelation(
        'Objective', related_query_name='assign_to_to_objectives')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.objective_name}"

    def generate_objective_name(self):
        #  time remaining until the deadline
        now = timezone.now()

        # Calculate time remaining until the deadline
        time_remaining = self.deadline - now

        """ 
        When dealing with a DateTimeField, ensure that both self.deadline and datetime.now() 
        are either naive or aware of timezones. we can make datetime.now() timezone aware by 
        using Django's timezone module.
        """

        if time_remaining.total_seconds() <= 0:
            time_remaining_str = "0 days"
        else:
            # format time remaining
            days = time_remaining.days
            weeks = days // 7
            if weeks > 0:
                time_remaining_str = f"{weeks} {'week' if weeks == 1 else 'weeks'}"
                days %= 7
                if days > 0:
                    time_remaining_str += f" {days} {'day' if days == 1 else 'days'}"
            else:
                time_remaining_str = f"{days} {'day' if days == 1 else 'days'}"

        #  objective name
        objective_name = f"{self.action_phrase} {self.number} {self.units} by {self.deadline.strftime('%B %d, %Y')} "
        objective_name += f"({time_remaining_str} remaining)"

        return objective_name

    # override the save method
    def save(self, *args, **kwargs):

        if not self.objective_name:  # check if objective_name is null
            # concatenate the desired fields for the default value
            self.objective_name = self.generate_objective_name()

        # make sure start_date is not further than deadline
        if self.deadline and self.start_date and self.deadline < self.start_date:
            raise ValidationError(
                "Deadline cannot be earlier than the start date.")
        # check if start_date is further than end_date
        if self.end_date and self.start_date and self.end_date < self.start_date:
            # set the end_date to the deadline
            self.end_date = self.deadline

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

        # update the status field depending on the date
        # check if the objective is in progress
        if self.start_date <= timezone.now() <= self.end_date and self.status != 'Completed':
            self.status = 'In Progress'
        # # check if the objective is completed
        # elif timezone.now() >= self.deadline:
        #     self.status = 'Completed'

        # manage completion_date
        # if the status has changed to "Completed" update the completion_date to the current datetime
        if self.status == 'Completed' and self.completion_date is None:
            self.completion_date = timezone.now()
        elif self.status != 'Completed':
            # keep  it to None
            self.completion_date = None
        # on renvoit la main à la méthode save originale
        super().save(*args, **kwargs)


start_date = datetime(2024, 1, 1)  # Example start date
end_date = datetime(2024, 1, 31)    # Example end date


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
    repeat_frequency = [('Daily', 'Daily'), ('Weekly',
                                             'Weekly'), ('Monthly', 'Monthly')]
    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(null=False, blank=False)
    number = models.DecimalField(max_digits=10, decimal_places=1, null=False, blank=False, validators=[
                                 MinValueValidator(Decimal('0.01'), "Amount must be a positive interger")])
    unit = models.CharField(max_length=50, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    frequency = models.CharField(
        choices=repeat_frequency, max_length=300, default='Daily')
    # the associated objectives
    objective = models.ForeignKey(
        Objective, blank=True, null=True, related_name="objective_kpis", on_delete=models.CASCADE)
    # how do you know a kpi is completed, evaluate it??
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


# Operational Goal
        """
        An operational goal has one or many objectives related to.
        An operational goal is assigned to a user who can created all the objectives
        
        for that operational goal
        """


class OperationalGoal(models.Model):

    priorities = [('Low', 'Low'), ('Intermediate',
                                   'Intermediate'), ('High', 'High')]

    objective_types = [('Financial', 'Financial'),
                       ('Non-Financial', 'Non-Financial')]

    status_choices = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]

    name = models.CharField(max_length=1000, blank=True, null=True)
    description = models.TextField()
    goal_type = models.CharField(choices=objective_types, max_length=300)
    priority = models.CharField(choices=priorities, max_length=300)
    start_date = models.DateTimeField(null=False)
    end_date = models.DateTimeField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    assign_to = models.ManyToManyField(
        to=User,  related_name="op_goal_assigned_to", blank=True)
    visible_to = models.ManyToManyField(
        to=User,  related_name="op_goal_visible_to", blank=True)
    # all the objectives related to an operational goal
    """ 
    operational_goal = OperationalGoal.objects.get(id=1)
    objectives = operational_goal.objectives.all()
    """
    # retrieve the user's operational goals
    """ 
    user = User.objects.get(username='example_user')
    operational_goals = user.op_goal_assigned_to.all()
    """


{
    "objective_name": "Test Objective",
    "assign_to": [1, 2],
    "visible_to": [1],
    "associated_task": "create the form",
    "evaluator": 1,
    "repeat_date": "Weekly",
    "deadline": "2024-02-11T12:00:00Z",
    "action_phrase": "Test Action",
    "number": 5,
    "units": "Test Units",
    "start_date": "2024-01-04T08:00:00Z",
    "end_date": "2024-10-31T18:00:00Z",
    "priority": "High",
    "complexity": "Hard",
    "objective_type": "Financial",
    "skills": [1, 2],
    "tools": [3],
    "dog": "the thing is working",
    "is_draft": False,
    "repeat": True
}

# to keep track of the changes in Objective object
class ObjectiveAuditLog(models.Model):
    objective = models.ForeignKey('Objective', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    changes = models.TextField()

    def __str__(self):
        return f"{self.objective} - {self.timestamp}"