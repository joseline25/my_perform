from rest_framework import serializers
from objective.models import Objective, Team, KPI
from action.models import Action
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
        
        


# KPI

class KPISerializer(serializers.ModelSerializer):
    class  Meta:
        model = KPI
        fields = '__all__'