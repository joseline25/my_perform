from rest_framework import serializers
from objective.models import Objective, Team, Skill, Tool, DefinitionOfGood
from action.models import Action, Question, Achievement
from django.contrib.auth.models import User


# User
class UserSerializer(serializers.ModelSerializer):
    class  Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

#Tool
class ToolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tool
        fields = ['tool_name']


#Skill
class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['skill_name']

#DefinitionOfGood
class DefinitionOfGoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = DefinitionOfGood
        fields = ['dog_criteria']



# Objective
class ObjectiveSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True)
    tools = ToolSerializer(many=True)
    dog = DefinitionOfGoodSerializer(many=True)
    assign_to = UserSerializer(many=True)
    visible_to = UserSerializer(many=True)
    evaluator = UserSerializer(many=False)
    
    class  Meta:
        model = Objective
        fields = '__all__'


# Team
class TeamSerializer(serializers.ModelSerializer):
    class  Meta:
        model = Team
        fields = '__all__'

#Questions
class QuestionSerializer(serializers.ModelSerializer):
    class  Meta:
        model = Question
        fields = '__all__'       

# Action       
class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = '__all__'
            
        




