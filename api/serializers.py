from rest_framework import serializers
from objective.models import Objective, Team, KPI, Skill, Tool, DefinitionOfGood, Skill, Tool
from objective.models_additional.task import Task
from action.models import Action, Question, Achievement
from django.contrib.auth.models import User


# User
class UserSerializer(serializers.ModelSerializer):
    class  Meta:
        model = User
        fields = [ 'first_name', 'last_name', 'email']

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
    assign_to = UserSerializer()
    visible_to = UserSerializer()
    evaluator = UserSerializer()
    
    class  Meta:
        model = Objective
        fields = '__all__'


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
    teams =TeamSerializer(many=True)
    class Meta:
        model = Tool
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        
        
# Objective



        
    # def get_created_at(self, obj):
    #     # Modify the representation of your datetime field here
    #     formatted_datetime = obj.created_at.strftime("%b %d, %Y %I:%M %p")
    #     return formatted_datetime





# Action

#Questions
class QuestionSerializer(serializers.ModelSerializer):
    class  Meta:
        model = Question
        fields = '__all__'       

#Achievements
class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model=Achievement
        fields = '__all__'

# Action       
class ActionSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True)
    tools = ToolSerializer(many=True)
    achievements = AchievementSerializer(many=True)
    questions = QuestionSerializer()
    collaborators = UserSerializer()
    added_by = UserSerializer()
    
    class Meta:
        model = Action
        fields = '__all__'
            
        

        
        


# KPI

class KPISerializer(serializers.ModelSerializer):
    class Meta:
        model = KPI
        fields = '__all__'

