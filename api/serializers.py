from rest_framework import serializers
from objective.models import Objective, Team
from action.models import Action, Question
from django.contrib.auth.models import User

# Objective
class ObjectiveSerializer(serializers.ModelSerializer):
    class  Meta:
        model = Objective
        fields = '__all__'


# Team
class TeamSerializer(serializers.ModelSerializer):
    class  Meta:
        model = Team
        fields = '__all__'
        

# Action       
class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = '__all__'
            
        
# User
class UserSerializer(serializers.ModelSerializer):
    class  Meta:
        model = User
        fields = '__all__'

#Questions
class QuestionSerializer(serializers.ModelSerializer):
    class  Meta:
        model = Question
        fields = '__all__'
