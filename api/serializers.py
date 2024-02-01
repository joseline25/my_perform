from rest_framework import serializers
from objective.models import Objective, Team, KPI, Skill, Tool, Skill, Tool
from objective.models_additional.task import Task
from action.models import Action, Question
from django.contrib.auth.models import User


# User
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


# Skill
class SkillSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = Skill
        fields = ['skill_id', 'skill_name', 'skill_description']

# Team


class TeamSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True)
    created_by = UserSerializer()
    users = UserSerializer(many=True)

    class Meta:
        model = Team
        fields = '__all__'


# Tool
class ToolSerializer(serializers.ModelSerializer):
    
    

    class Meta:
        model = Tool
        fields = ['tool_id', 'tool_name', 'description']


# Objective
class ObjectiveSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True)
    tools = ToolSerializer(many=True)
    assign_to = UserSerializer(many=True)
    visible_to = UserSerializer(many=True)
    evaluator = UserSerializer()

    class Meta:
        model = Objective
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = '__all__'


# Objective

class ObjectiveSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True)
    tools = ToolSerializer(many=True)
    assign_to = UserSerializer(many=True)
    visible_to = UserSerializer(many=True)
    

    class Meta:
        model = Objective
        fields = '__all__'


# Questions
class QuestionSerializer(serializers.ModelSerializer):
    objective = ObjectiveSerializer()

    class Meta:
        model = Question
        fields = '__all__'


# Action
class ActionSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True)
    tools = ToolSerializer(many=True)
    collaborators = UserSerializer(many=True)
    added_by = UserSerializer()
    objective = ObjectiveSerializer()

    class Meta:
        model = Action
        fields = '__all__'


# KPI

class KPISerializer(serializers.ModelSerializer):
    objective = ObjectiveSerializer()

    class Meta:
        model = KPI
        fields = '__all__'
