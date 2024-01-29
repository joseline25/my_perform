from rest_framework import serializers
from objective.models import Objective, Team, KPI, Skill, Tool
from objective.models_additional.task import Task
from action.models import Action
from django.contrib.auth.models import User


# User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

# Skill

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'


# Team
class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'

# Tool
class ToolSerializer(serializers.ModelSerializer):
    teams =TeamSerializer(many=True)
    class Meta:
        model = Tool
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
    associated_task = TaskSerializer(many=True)
    
    # Datetime fields formatting 
    
    #created_at = serializers.SerializerMethodField()

    class Meta:
        model = Objective
        fields = '__all__'
        
    # def get_created_at(self, obj):
    #     # Modify the representation of your datetime field here
    #     formatted_datetime = obj.created_at.strftime("%b %d, %Y %I:%M %p")
    #     return formatted_datetime





# Action
class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = '__all__'
        
        


# KPI

class KPISerializer(serializers.ModelSerializer):
    objective = ObjectiveSerializer()
    class Meta:
        model = KPI
        fields = '__all__'
