from rest_framework import serializers
from objective.models import Objective, OperationalGoal, Team, KPI, Skill, Tool, Skill, Tool, ObjectiveAuditLog
from objective.models_additional.task import Task
from action.models import Action, Question, ActionMainEntry
from django.contrib.auth.models import User
from django.utils import timezone


# User GET
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']

# User POST


class UserSerialiazerPost(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

# Skill GET


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['skill_id', 'skill_name', 'skill_description']

# Skill POST


class SkillSerialiserPost(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'
    # change the update_at field when doing update

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        instance.updated_at = timezone.now()
        instance.save()
        return instance

# Team GET


class TeamSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True)
    created_by = UserSerializer()
    users = UserSerializer(many=True)

    class Meta:
        model = Team
        fields = '__all__'


# Team POST

class TeamSerializerPost(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'
    # change the update_at field when doing update

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        # update updated_at field
        instance.updated_at = timezone.now()
        instance.save()
        return instance

# Tool GET


class ToolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tool
        fields = ['tool_id', 'tool_name', 'description']

# Tool POST


class ToolSerializerPost(serializers.ModelSerializer):
    class Meta:

        model = Tool
        fields = '__all__'

    # change the update_at field when doing update
    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        # update updated_at field
        instance.updated_at = timezone.now()
        instance.save()
        return instance




# OperationalGoal GET
class OperationalGoalSerializer(serializers.ModelSerializer):
    assign_to = UserSerializer(many=True)
    visible_to = UserSerializer(many=True)
    class Meta:
        model = OperationalGoal
        fields = '__all__'
        
# OperationalGoal POST
class OperationalGoalSerializerPost(serializers.ModelSerializer):
    
        model = OperationalGoal
        fields = '__all__'


# Objective GET


class ObjectiveSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True)
    tools = ToolSerializer(many=True)
    assign_to = UserSerializer(many=True)
    visible_to = UserSerializer(many=True)
    evaluator = UserSerializer()
    operational_goal = OperationalGoalSerializer()

    class Meta:
        model = Objective
        fields = '__all__'

# Objective POST


class ObjectiveSerializerPost(serializers.ModelSerializer):
    # initialize changes dictionary to keep track of every updates
    
    changes = {}

    class Meta:
        model = Objective
        fields = '__all__'

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)

        # update updated_at field
        instance.updated_at = timezone.now()
        instance.save()

        # keep track of all updates
        old_instance = self.Meta.model.objects.get(pk=instance.pk)

        for attr, value in validated_data.items():
            if getattr(instance, attr) != value:
                # Add new changes to the existing changes dictionary
                # changes is in ObjectiveAuditLog!!
                self.changes[attr] = {
                    'old_value': getattr(old_instance, attr),
                    'new_value': value
                }

        # Create audit log entry
        # user=self.context['request'].user,
        ObjectiveAuditLog.objects.create(
            objective=instance, changes=self.changes)
        return instance




#ObjectiveAuditLog
class ObjectiveAuditLogSerializer(serializers.ModelSerializer):
    
    # user = UserSerializer()
    # objective = ObjectiveSerializer()
    class Meta:
        model = ObjectiveAuditLog
        fields = '__all__'

# Objective POST


class ObjectiveAuditLogSerializerPost(serializers.ModelSerializer):
    
    class Meta:
        model = ObjectiveAuditLog
        fields = '__all__'

# Task GET and POST
class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = '__all__'


# Questions GET
class QuestionSerializer(serializers.ModelSerializer):
    objective = ObjectiveSerializer()

    class Meta:
        model = Question
        fields = '__all__'

# Question POST


class QuestionSerializerPost(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


# Action Get
class ActionSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True)
    tools = ToolSerializer(many=True)
    collaborators = UserSerializer(many=True)
    added_by = UserSerializer()
    objective = ObjectiveSerializer()

    class Meta:
        model = Action
        fields = '__all__'

# Action POST


class ActionSerializerPost(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = '__all__'


# ActionMainEntry Get
class ActionMainEntrySerializer(serializers.ModelSerializer):
    collaborators = UserSerializer(many=True)
    objective = ObjectiveSerializer()

    class Meta:
        model = ActionMainEntry
        fields = '__all__'

# ActionMainEntry POST


class ActionMainEntryPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActionMainEntry
        fields = '__all__'


# KPI GET

class KPISerializer(serializers.ModelSerializer):
    objective = ObjectiveSerializer()

    class Meta:
        model = KPI
        fields = '__all__'


# KPI POST

class KPISerializerPost(serializers.ModelSerializer):
    class Meta:
        model = KPI
        fields = '__all__'
