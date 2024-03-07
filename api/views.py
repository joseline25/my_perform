from django.db.models import Sum
from collections import Counter
from datetime import timedelta
from django.db import transaction
from datetime import datetime
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import ObjectiveSerializer, ObjectiveSerializerPost, ActionSerializer, ActionSerializerPost, TeamSerializer, TeamSerializerPost, KPISerializer, KPISerializerPost, QuestionSerializer, ToolSerializer, ToolSerializerPost, SkillSerializer, SkillSerialiserPost, TaskSerializer,  ActionMainEntrySerializer, ActionMainEntryPostSerializer, UserSerialiazerPost, OperationalGoalSerializer, OperationalGoalSerializerPost, ObjectiveAuditLogSerializer, ObjectiveAuditLogSerializerPost
from objective.models import Objective, Team, UserTeam, KPI, Tool, Skill, OperationalGoal
from objective.models_additional.task import Task
from action.models import Action, Question, ActionMainEntry
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.db.models import Count
import io
import base64

import matplotlib.pyplot as plt


# additionals method to compute metrics
from .metrics import *


# Objective

# GET all

@api_view(['GET'])
def all_objectives(request):
    objectives = Objective.objects.all()
    objectives_serializer = ObjectiveSerializer(objectives, many=True)

    users = User.objects.all()
    users_serializer = UserSerializer(users, many=True)

    response_data = {
        'objectives': objectives_serializer.data,
        'users': users_serializer.data
    }

    return Response(response_data)


# GET id
@api_view(['GET'])
def objective_detail(request, objective_id):
    try:
        objective = Objective.objects.get(objective_id=objective_id)
    except Objective.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ObjectiveSerializer(objective)
    return Response(serializer.data)

# GET objectives changes


@api_view(['GET'])
def objective_update_changes(request, objective_id):
    try:
        objective = Objective.objects.get(objective_id=objective_id)
    except Objective.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    changes = objective.objectives_changes.all()
    serializer = ObjectiveAuditLogSerializer(changes, many=True)
    return Response(serializer.data)


# POST

@api_view(['POST'])
def create_objective(request):
    serializer = ObjectiveSerializerPost(data=request.data)
    if serializer.is_valid():

        print("Validated Data:", serializer.validated_data)

        # save
        new_objective = serializer.save()

        # many to many fields
        new_objective.assign_to.set(serializer.validated_data.get('assign_to'))
        new_objective.visible_to.set(
            serializer.validated_data.get('visible_to'))

        new_objective.skills.set(serializer.validated_data.get('skills'))
        new_objective.tools.set(serializer.validated_data.get('tools'))

        return Response({'status': 'success', 'message': 'Objective created successfully'}, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# PUT
@api_view(['PUT'])
def update_objective(request, objective_id):
    try:
        objective = Objective.objects.get(objective_id=objective_id)
    except Objective.DoesNotExist:
        return Response({"message": "No objective found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = ObjectiveSerializerPost(
        objective, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response({"message": "Objective successfilly updated"}, serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# DELETE


@api_view(['DELETE'])
def delete_objective(request, objective_id):
    try:
        with transaction.atomic():
            objective = Objective.objects.get(pk=objective_id)

            # Clear many-to-many relations
            objective.assign_to.clear()
            objective.visible_to.clear()
            objective.skills.clear()
            objective.tools.clear()

            # Delete the objective
            objective.delete()

            return Response({"message": "Objective and related relations deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    except Objective.DoesNotExist:
        return Response({"message": "No Objective found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"message": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Action
# GET all


@api_view(['GET'])
def all_actions(request):
    actions = Action.objects.all()
    serializer = ActionSerializer(actions, many=True)
    return Response(serializer.data)

# list of actions for a specific objective


@api_view(["GET"])
def action_objective(request, objective_id):
    try:
        objective = Objective.objects.get(objective_id=objective_id)

    except Objective.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    actions = objective.action_entry.all()

    serializer = ActionMainEntrySerializer(actions, many=True)
    return Response(serializer.data)


# action details
@api_view(["GET"])
def action_details(request, id):
    try:
        action = Action.objects.get(id=id)
    except Action.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ActionSerializer(action)
    return Response(serializer.data)


@api_view(['PUT'])
def update_action(request, id):
    try:
        action = Action.objects.get(id=id)
    except Action.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = ActionSerializerPost(
            action, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({'error': 'Invalid HTTP method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['Delete'])
def delete_action(request, id):
    try:
        action = Action.objects.get(id=id)
    except Action.DoesNotExist:
        return Response({"message": "No action found"}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'Delete':
        action.delete()
        return Response({"message": "Action deleted"}, status=status.HTTP_204_NO_CONTENT)
    return Response({'error': 'Invalid HTTP method'}, status.HTTP_405_METHOD_NOT_ALLOWED)


# list of questions for an objective

@api_view(['GET'])
def questions(request, objective_id):
    try:
        questions = Question.objects.filter(objective=objective_id)
    except Question.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = QuestionSerializer(questions)
    return Response(serializer.data)


# create an action


@api_view(['POST'])
def create_action(request):
    serializer = ActionSerializerPost(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


# list of teams
@api_view(['GET'])
def all_teams(request):
    teams = Team.objects.all()
    serializer = TeamSerializer(teams, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def create_team(request):
    serializer = TeamSerializerPost(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


# team details
@api_view(["GET"])
def team_details(request, id):
    try:
        team = Team.objects.get(id=id)
    except Team.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ActionSerializer(team)
    return Response(serializer.data)


# get all the users of a team
@api_view(['GET'])
def team_users(request, id):
    try:
        team = Team.objects.get(id=id)
    except Team.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = TeamSerializer(team)
    return Response(serializer.data['users'])


# Users

# create a new user ()
@api_view(['POST'])
def create_user(request):
    serializer = UserSerialiazerPost(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# get all the users


@api_view(['GET'])
def all_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


# get details of a user
@api_view(['GET'])
def user_detail(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = UserSerializer(user)
    return Response(serializer.data)


# get the users in the same team as a specific user
@api_view(['GET'])
def users_in_same_team(request, user_id):
    try:
        # get the user
        user = User.objects.get(id=user_id)
        # get allthe users of his team
        user_teams = Team.objects.filter(userteam__user=user)
        # filter all the other users except user
        users_in_same_team = User.objects.filter(
            userteam__team__in=user_teams).exclude(id=user_id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = UserSerializer(users_in_same_team, many=True)
    return Response(serializer.data)


# list of kpis for an objective


@api_view(['GET', 'POST'])
def kpi_list_create(request, objective_id):
    objective = get_object_or_404(Objective, objective_id=objective_id)

    if request.method == 'GET':
        # serialize the objective details and the KPIs
        objective_serializer = ObjectiveSerializer(objective)
        kpis = KPI.objects.filter(objective=objective)
        kpi_serializer = KPISerializer(kpis, many=True)

        response_data = {
            'objective': objective_serializer.data,
            'kpis': kpi_serializer.data
        }

        return Response(response_data)

    elif request.method == 'POST':
        serializer = KPISerializerPost(data=request.data)

        if serializer.is_valid():
            serializer.save(objective=objective)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# create a kpi indepedently
@api_view(['POST'])
def create_kpi(request):
    serializer = KPISerializerPost(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


{"name": "kpi_1",
 "description": "the first kpis to test the KPI form",
 "number": 3,
 "frequency": "Weekly",
 "unit": 1,
 "objective": 1}


# get all the kpis
@api_view(['GET'])
def kpis_all(request):
    kpis = KPI.objects.all()
    kpi_serializer = KPISerializer(kpis, many=True)
    return Response(kpi_serializer.data)

# update a kpi


@api_view(['PUT'])
def update_kpi(request, id):
    try:
        kpi = KPI.objects.get(id=id)
    except KPI.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        serializer = KPISerializerPost(kpi, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({'error': 'Invalid HTTP method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['DELETE'])
def delete_kpi(request, id):
    try:
        kpi = KPI.objects.get(id=id)
    except KPI.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'DELETE':
        kpi.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response({'error': 'Invalid HTTP method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

# kpi details


@api_view(["GET"])
def kpi_details(request, id):
    try:
        kpi = KPI.objects.get(id=id)
    except KPI.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = KPISerializer(kpi)
    return Response(serializer.data)


@api_view(['GET'])
def all_tools(request):
    tools = Tool.objects.all()
    serializer = ToolSerializer(tools, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def create_tool(request):
    serializer = ToolSerializerPost(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['POST'])
def create_skill(request):
    serializer = SkillSerialiserPost(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


# create task

@api_view(['POST'])
def create_task(request):
    serializer = TaskSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


# task details
@api_view(["GET"])
def task_details(request, id):
    try:
        task = Task.objects.get(id=id)
    except Task.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = TaskSerializer(task)
    return Response(serializer.data)


# tool details
@api_view(["GET"])
def tool_details(request, id):
    try:
        tool = Tool.objects.get(tool_id=id)
    except Tool.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ToolSerializer(tool)
    return Response(serializer.data)

# skill details


@api_view(["GET"])
def skill_details(request, skill_id):
    try:
        skill = Skill.objects.get(skill_id=skill_id)
    except Skill.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ToolSerializer(skill)
    return Response(serializer.data)


@api_view(['GET'])
def get_skills(request):
    skills = Skill.objects.all()
    serializer = SkillSerializer(skills, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_all_tasks(request):
    tasks = Task.objects.all()
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)


@api_view(['PUT'])
def update_tool(request, tool_id):
    try:
        tool = Tool.objects.get(id=tool_id)
    except Tool.DoesNotExist:
        return Response({"message": "No tool found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = ToolSerializer(tool, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response({"message": "Tool successfilly updated"}, serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_tool(request, tool_id):
    try:
        tool = Tool.objects.get(id=tool_id)
    except Tool.DoesNotExist:
        return Response({"message": "No Tool found"}, status=status.HTTP_404_NOT_FOUND)

    tool.delete()
    return Response({"message": "Tool deleted"}, tatus=status.HTTP_204_NO_CONTENT)

# update a skill


@api_view(['PUT'])
def update_skill(request, skill_id):
    try:
        skill = Skill.objects.get(skill_id=skill_id)
    except Skill.DoesNotExist:
        return Response({"message": "No skill found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = SkillSerializer(skill, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response({"message": "Skill updated succesfully"}, serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# update task


@api_view(['PUT'])
def update_task(request, id):
    try:
        task = Task.objects.get(id=id)
    except Task.DoesNotExist:
        return Response({"message": "No task found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = TaskSerializer(task, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response({"message": "task updated succesfully"}, serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_skill(request, skill_id):
    try:
        skill = Skill.objects.get(skill_id=skill_id)
    except Skill.DoesNotExist:
        return Response({"message": "No skill found"}, status=status.HTTP_404_NOT_FOUND)

    skill.delete()
    return Response({"message": "Skill deleted "}, status=status.HTTP_204_NO_CONTENT)


@api_view(['DELETE'])
def delete_task(request, id):
    try:
        task = Task.objects.get(id=id)
    except Task.DoesNotExist:
        return Response({"message": "No task found"}, status=status.HTTP_404_NOT_FOUND)

    task.delete()
    return Response({"message": "Task deleted "}, status=status.HTTP_204_NO_CONTENT)


@api_view(['PUT'])
def update_user(request, id):
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return Response({"message": "No user found with this id"}, status=status.HTTP_404_NOT_FOUND)

    serializer = UserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User saved successfully"})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"message": "No user found with this id"}, status=status.HTTP_404_NOT_FOUND)
    user.delete()
    return Response({"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['PUT'])
def update_team(request, id):
    try:
        team = Team.objects.get(id=id)
    except Team.DoesNotExist:
        return Response({"message": "Team not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = TeamSerializer(team, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Team updated successfully"}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# PUT (Action Main Entry)
@api_view(['PUT'])
def action_main_entry_update(request, id):
    try:
        team = ActionMainEntry.objects.get(id=id)
    except ActionMainEntry.DoesNotExist:
        return Response({"message": "Action not found!"}, status=status.HTTP_404_NOT_FOUND)
    serializer = ActionMainEntryPostSerializer(
        team, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Action updated successfully"}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# DELETE (Action Main Entry)
@api_view(['DELETE'])
def delete_action_main_entry(request, id):
    try:
        action = ActionMainEntry.objects.get(id=id)
    except ActionMainEntry.DoesNotExist:
        return Response({"message": "Action not found!"}, status=status.HTTP_404_NOT_FOUND)
    action.delete()
    return Response({"message": "Action deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['DELETE'])
def delete_team(request, id):
    try:
        team = Team.objects.get(id=id)
    except Team.DoesNotExist:
        return Response({"message": "Team not found"}, status=status.HTTP_404_NOT_FOUND)

    team.delete()
    return Response({"message": "Team deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


# Main Action Entry

# create an action entry
@api_view(['POST'])
def create_action_main_entry(request):
    if request.method == 'POST':
        serializer = ActionMainEntryPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# all actions for a particular date


@api_view(['GET'])
def get_actions_for_date(request, date):
    try:
        # date string to datetime object
        date_ = datetime.strptime(date, '%Y-%m-%d').date()

        # get all actions for the specific date
        actions = ActionMainEntry.objects.filter(date=date_)
        serializer = ActionMainEntrySerializer(actions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except ValueError:
        # if invalid date format
        return Response({'error': 'Invalid date format. Use YYYY-MM-DD.'}, status=status.HTTP_400_BAD_REQUEST)


# all actions within a specified time frame

@api_view(['GET'])
def get_actions_in_timeframe(request, start_date, end_date):
    try:
        # convert start and end date strings to datetime objects
        start_date_ = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date_ = datetime.strptime(end_date, '%Y-%m-%d').date()

        # get all actions within the time frame
        actions = ActionMainEntry.objects.filter(
            date__range=(start_date_, end_date_))
        serializer = ActionMainEntrySerializer(actions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except ValueError:
        # if invalid date format
        return Response({'error': 'Invalid date format. Use YYYY-MM-DD.'}, status=status.HTTP_400_BAD_REQUEST)

# get all the actions of an objective


@api_view(["GET"])
def action_main_entry_objective(request, objective_id):
    try:
        actions = ActionMainEntry.objects.filter(objective=objective_id)
    except ActionMainEntry.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = ActionMainEntrySerializer(actions, many=True)
    return Response(serializer.data)

# GET id (Action Main Entry row)


@api_view(["GET"])
def action_main_entry_details(request, id):
    try:
        action = ActionMainEntry.objects.get(id=id)
    except ActionMainEntry.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = ActionMainEntrySerializer(action)
    return Response(serializer.data)

# get all the actions in the system


@api_view(["GET"])
def action_main_entry_all(request):

    actions = ActionMainEntry.objects.all()

    serializer = ActionMainEntrySerializer(actions, many=True)
    return Response(serializer.data)


# publish an objective

@api_view(['POST'])
def publish_objective(request, objective_id):
    try:
        objective = Objective.objects.get(objective_id=objective_id)
    except Objective.DoesNotExist:
        return Response({"message": "Objective not found"}, status=status.HTTP_404_NOT_FOUND)

    # change is_published field to True
    objective.is_published = True
    objective.save()

    return Response({"message": "Objective published successfully"}, status=status.HTTP_200_OK)

# list of published objectives


@api_view(['GET'])
def published_objectives(request):

    published_objectives = Objective.objects.filter(is_published=True)
    serializer = ObjectiveSerializer(published_objectives, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# list of completed objectives ( objectives that have a value in the completion date field)


@api_view(['GET'])
def completed_objectives(request):
    #  all completed objectives (where completion_date is not null)
    # completed_objectives = Objective.objects.exclude(completion_date__isnull=True)
    completed_objectives = Objective.objects.filter(status='Completed')
    serializer = ObjectiveSerializer(completed_objectives, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# Get op goals assigned to a aser and get all objectives related to those op goals

@api_view(['GET'])
def objectives_assigned_to_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        # Total Numer of Goals
        op_goals = OperationalGoal.objects.filter(assign_to=user_id)
        op_goals_count = op_goals.count()
        # Total Number of Objectives
        objectives = Objective.objects.filter(operational_goal__in=op_goals)
        objectives_count = objectives.count()
        #  completed objectives within
        completed_objectives = objectives.filter(status='Completed')
        completed_objectives_count = completed_objectives.count()
        # Goal Progress
        goal_progress = (completed_objectives_count/objectives_count)*100

        serializer_op_goals = OperationalGoalSerializer(op_goals, many=True)
        serializer_objectives = ObjectiveSerializer(objectives, many=True)
        serializer_completed_objectives = ObjectiveSerializer(
            completed_objectives, many=True)

        # Get all users assigned to the objectives of the operational goals: Number of Supervisees
        # exclude the user with user_id
        users_assigned = User.objects.filter(
            Q(objectives_assigned_to__operational_goal__in=op_goals) & ~Q(id=user_id)).distinct()

        data = {
            'user': UserSerializer(user).data,
            'operational_goals': serializer_op_goals.data,
            'all_objectives': serializer_objectives.data,
            'completed_objectives': serializer_completed_objectives.data,
            'goal_progress': goal_progress,
            'operational_goals_count': op_goals_count,
            'objectives_count': objectives_count,

        }
        return Response(data)
    except OperationalGoal.DoesNotExist:
        return Response({"message": "Operational goals not found"}, status=status.HTTP_404_NOT_FOUND)

# Get all completed objectives related to an operational goal


@api_view(['GET'])
def completed_objectives_for_op_goal(request, op_goal_id):
    try:
        objectives = Objective.objects.filter(
            operational_goal=op_goal_id, status='Completed')
        serializer = ObjectiveSerializer(objectives, many=True)
        return Response(serializer.data)
    except Objective.DoesNotExist:
        return Response({"message": "Objectives not found"}, status=status.HTTP_404_NOT_FOUND)

# Objective Progress , transform this to a method of the model Objective


@api_view(['GET'])
def objective_progress(request, objective_id):
    try:
        #  KPIs related to the objective
        kpis = KPI.objects.filter(objective_id=objective_id)
        serializer = KPISerializer(kpis, many=True)

        #  KPIs completed within
        # kpis_completed = KPI.objects.filter(kpi__in=kpis)
        # work on the KPI model

        serializer = KPISerializer(kpis, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except KPI.DoesNotExist:
        return Response({"message": "KPIs not found for the objective"}, status=status.HTTP_404_NOT_FOUND)


# Dashboard

# Employee
# current date
current_date = timezone.now()
# current date 7 days before
current_date_previous = current_date - timedelta(days=7)


#@api_view(['POST'])
@api_view(['GET'])
def employee_dashboard(request, user_id):
    # get values from request data
    # user_id = request.data.get('user_id')
    # start_date_str = request.data.get('start_date')
    # end_date_str = request.data.get('end_date')
    current_date = timezone.now()
    current_date_previous = current_date - timedelta(days=7)
    start_date= current_date_previous
    end_date = current_date


    # Calculate default start date and end date if not provided
    # current_date = timezone.now()
    # current_date_previous = current_date - timedelta(days=7)
    # start_date = datetime.strptime(
    #     start_date_str, '%Y-%m-%d') if start_date_str else current_date_previous
    # end_date = datetime.strptime(
    #     end_date_str, '%Y-%m-%d') if end_date_str else current_date


    # get the user
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    # list of all actions in that timeframe:
    actions = ActionMainEntry.objects.filter(
        name=user,
        date__range=[start_date, end_date]
    )

    # Total Actions Approved : filter actions based on the time frame and status == "Validated"
    total_approved_actions = ActionMainEntry.objects.filter(
        name=user,
        status='Validated',
        date__range=[start_date, end_date]
    )
    total_approved_actions_count = total_approved_actions.count()

    # Total Actions Rejected : filter actions based on the time frame and status == "Rejected"
    total_rejected_actions = ActionMainEntry.objects.filter(
        name=user,
        status='Rejected',
        date__range=[start_date, end_date]
    )

    total_rejected_actions_count = total_rejected_actions.count()

    # Total Actions Pending in review: status == "Pending"
    total_pending_actions = ActionMainEntry.objects.filter(
        name=user,
        status='Pending',
        date__range=[start_date, end_date]
    )

    total_pending_actions_count = total_pending_actions.count()

    # Top collaborators
    collaborators_list = [
        collaborator for action in actions for collaborator in action.collaborators.all()]
    # Count occurrences of each collaborator
    collaborators_count = Counter(collaborators_list)
    # Sort collaborators based on the number of occurrences
    sorted_collaborators = sorted(
        collaborators_count.items(), key=lambda x: x[1], reverse=True)

    # the objectives related to the  actions in the timeframe
    objectives_from_actions = Objective.objects.filter(
        action_entry__in=actions)
    # or objectives = set(action.objective for action in actions)
    #  list of collaborators from objectives related to actions
    collaborators_objectives_list = [
        collaborator for objective in objectives_from_actions for collaborator in objective.assign_to.all()]
    # count occurrences of each collaborator
    collaborators_objectives_count = Counter(collaborators_list)
    # sort collaborators based on the number of occurrences in the previous list
    sorted_collaborators_objectives = sorted(
        collaborators_objectives_count.items(), key=lambda x: x[1], reverse=True)

    # Achievement Tracker

    # get the rate of achievemnts for actions in the timeframe
    #  occurrences of each achievement_value
    achievements_count = Counter(action.achievements for action in actions)
    # total number of actions
    total_actions = len(actions)
    #  all possible achievement values
    all_achievement_values = dict(ActionMainEntry.achievements_values).keys()
    # compute the rate of actions for each achievement_value
    # rate_of_actions = {achievement_value: achievements_count.get(
    #     achievement_value, 0) / total_actions for achievement_value in all_achievement_values}

    rate_of_actions = {}
    if total_actions != 0:
        rate_of_actions = {achievement_value: achievements_count.get(
            achievement_value, 0) / total_actions for achievement_value in all_achievement_values}
    else:
        # Handle the case where there are no actions
        rate_of_actions = {achievement_value: 0 for achievement_value in all_achievement_values}
    # dates

    # Missed Action Tracker
    # alldates of actions
    action_dates = set(action.date.date() for action in actions)
    #  list of all dates within the specified timeframe
    all_dates = [start_date + timedelta(days=i)
                 for i in range((end_date - start_date).days + 1)]
    # get dates where no actions were entered
    missing_dates = [date for date in all_dates if date not in action_dates]

    # total time enterd
    # Sum the duration of all actions in filtered_actions
    total_duration = actions.aggregate(total_duration=Sum('duration'))[
        'total_duration']
    if total_duration is None:
        total_duration = 0

    total_duration_hours = total_duration // 60
    total_duration_minutes = total_duration % 60

    # tools used
    #  from related objectives
    unique_tools_set = set()
    for objective in objectives_from_actions:
        unique_tools_set.update(objective.tools.all())
    unique_tools_list = list(unique_tools_set)

    data = {'actions': ActionMainEntrySerializer(actions, many=True).data,
            'actions_count': actions.count(),
            'total_approved_actions': ActionMainEntrySerializer(total_approved_actions, many=True).data,
            'total_approved_actions_count': total_approved_actions_count,
            'total_rejected_actions': ActionMainEntrySerializer(total_rejected_actions, many=True).data,
            'total_rejected_actions_count': total_rejected_actions_count,
            'total_pending_actions': ActionMainEntrySerializer(total_pending_actions, many=True).data,
            'total_pending_actions_count': total_pending_actions_count,
            'actions_collaborators': UserSerializer(sorted_collaborators, many=True).data,
            'objectives_collaborators': UserSerializer(sorted_collaborators_objectives, many=True).data,
            'achievement_tracker': rate_of_actions,
            'all_dates': all_dates,
            'action_dates': action_dates,
            'missing_dates': missing_dates,
            'total_duration_hours': total_duration_hours,
            'total_duration_minutes': total_duration_minutes,
            'unique_tools': ToolSerializer(unique_tools_list, many=True).data,
            'top_collaborators_for_objectives': sorted_collaborators,
            'sorted_collaborators_objectives': UserSerializer(sorted_collaborators_objectives, many=True).data,
            'total_approved_actions': total_approved_actions,
            'objectives_assigned':ObjectiveSerializer(objectives_from_actions, many=True).data,
            'total_objectives_assigned': objectives_from_actions.count(),
            'user': UserSerializer(user).data,
            'start_date': start_date,
            'end_date': end_date,

            # optional
            'current_date': current_date,
            'current_date_previous': current_date_previous,
            }

    return Response(data)


@api_view(['GET'])
def supervisor_dashboard(request, user_id):

    # get the user
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # list of all objectives created by the supervisor
    objectives = Objective.objects.filter(created_by=user)

    # get total number of objectives
    total_number_objectives = objectives.count()
    # total number of supervisees : all the people assigned to those objectives
    # objectives_assignees = set(objective.assign_to.all() for objective in objectives)
    assigned_users_set = set()
    for objective in objectives:
        assigned_users_set.update(objective.assign_to.all())

    assigned_users = list(assigned_users_set)

    # assigned objectives to the supervisor
    objectives_assigned = Objective.objects.filter(assign_to=user)

    # get all actions related to the objectives created by the supervisor
    all_actions = []

    # Iterate through each objective to get related actions
    for objective in objectives:
        #  all actions related to the current objective
        actions = ActionMainEntry.objects.filter(objective=objective)
        # Add the actions to the list
        all_actions.extend(actions)

    # action control

    # count the occurrences of each status
    status_counts = Counter(action.status for action in all_actions)
    total_actions = len(all_actions)
    status_rates = {status: count / total_actions for status,
                    count in status_counts.items()}
    # add missing status with a rate of 0
    for status, _ in ActionMainEntry.status_choices:
        if status not in status_rates:
            status_rates[status] = 0

    # Achievement Tracker

    # get the rate of achievemnts for actions in the timeframe
    #  occurrences of each achievement_value
    achievements_count = Counter(action.achievements for action in all_actions)
    # total number of actions
    total_actions = len(actions)
    #  all possible achievement values
    all_achievement_values = dict(ActionMainEntry.achievements_values).keys()
    # compute the rate of actions for each achievement_value
    rate_of_actions = {achievement_value: achievements_count.get(
        achievement_value, 0) / total_actions for achievement_value in all_achievement_values}

    # plot the achievemnt rate
    x_values = list(rate_of_actions.keys())
    y_values = list(rate_of_actions.values())

    # plot the curve
    plt.figure(figsize=(10, 6))
    plt.plot(x_values, y_values, marker='o', linestyle='-')
    plt.xlabel('Achievement Values')
    plt.ylabel('Rate of Achievements')
    plt.title(' Achievements Tracker')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()

    # save the plot to a BytesIO buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # convert the plot to an  encoded string(base64)
    plot_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    # Close the plot to free up resources
    plt.close()

    data = {
        'user': user_id,
        'objectives': objectives,
        'total_number_objectives': total_number_objectives,
        'number_supervisees': assigned_users,
        'objectives_assigned': objectives_assigned,
        'activities_overview': all_actions,
        'action_control': status_rates,
        # I did not take into account last week or this week
        'achievement_tracker': rate_of_actions,
        'achievement_tracker_plot': plot_base64,


    }


# API views for Performance - Profuctivity metrics
""" 
Objective Achievement Rate (OAR) for an employee
OAR=[Completed Objectives/Assigned Objectives] * 100

"""


@api_view(['GET'])
def user_performance(request, user_id, start_date, end_date):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # get the list of all objectives assigned to the user with user_id in a timeframe

    list_1 = Objective.objects.filter(
        assign_to__id__in=user_id,
        start_date__lte=end_date,    # Objective starts before or on the end date
        end_date__gte=start_date     # Objective ends after or on the start date
    )
    list_1_count = list_1.count()

    # to include objectives that overlap with the timeframe
    # but don't necessarily start or end within it
    objectives = Objective.objects.filter(
        Q(assign_to__id__in=user_id),  # Filter by user IDs
        Q(start_date__lte=end_date) | Q(end_date__gte=start_date)
    )

    # get the list of completed objective
    # how do we know that an objective is completed? with the status field
    # Filter objectives completed by the user within the specified timeframe
    list_2 = Objective.objects.filter(
        assign_to__id__in=user_id,
        status='Completed',
        # objective's deadline is after or on start_date
        deadline__gte=start_date,
        deadline__lte=end_date                # objective's deadline is before or on end_date
    )

    list_2_count = list_2.count()

    # to include objectives that were completed within the timeframe
    # but don't necessarily have a deadline within it
    completed_objectives = Objective.objects.filter(
        Q(created_by=user_id),
        Q(status='Completed'),
        Q(deadline__gte=start_date) | Q(deadline__lte=end_date)
    )

    # Objective Achievement Rate (OAR)
    if list_1_count > 0:
        oar = (list_2_count / list_1_count) * 100
    else:
        oar = 0
    data = {
        'user': UserSerializer(user).data,
        'completed_objectives': list_2,
        'assigned_objectives': list_1,
        'completed_objectives_count': list_2_count,
        'assigned_objectives_count': list_1_count,
        'oar': oar
    }

    return Response(data)


""" 
Average Number of Actions per Objective

"""


@api_view(['GET'])
def average_actions_per_objective(request, user_id, start_date, end_date):
    # get the user
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # retrieve all actions related to objectives in timeframe
    actions = ActionMainEntry.objects.filter(
        objective__start_date__lte=end_date,
        objective__end_date__gte=start_date,
        # if user_id is in the assign_to list
        objective__assign_to__in=[user_id]

    )

    # total
    total_actions = actions.count()

    # number of objectives
    total_objectives = Objective.objects.filter(
        assign_to__id__in=user_id,
        start_date__lte=end_date,
        end_date__gte=start_date
    ).count()

    # ANA/O
    if total_objectives > 0:
        average_actions_per_objective = total_actions / total_objectives
    else:
        average_actions_per_objective = 0

    data = {
        'user': UserSerializer(user).data,
        'total_actions': total_actions,
        'total_objectives': total_objectives,
        'average_actions_per_objective': average_actions_per_objective
    }

    return Response(data)


""" 
Time to Objective Completion

Time to Objective Completion = Actual Completion Date-Objective Start Date
"""


@api_view(['GET'])
def time_objective_completion(request, objective_id):
    # get the user
    try:
        objective = Objective.objects.get(id=objective_id)
    except Objective.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # completion date of the objective
    completion_date = objective.completion_date
    # start date of the objective
    start_date = objective.start_date

    # get the time to objective completion
    if completion_date is None:
        return Response({"message": "The completion time of the objective is not set", "time_to_completion": -1}, status=status.HTTP_200_OK)
    else:

        time_to_completion = completion_date - start_date
        if time_to_completion.total_seconds() < 0:
            return Response({"message": "Objective has already been completed", "time_to_completion": -1}, status=status.HTTP_200_OK)
        else:
            return Response({"time_to_completion": time_to_completion.total_seconds()}, status=status.HTTP_200_OK)


""" 
Number of Objectives Assigned vs Completed

Objective Completion Rate (OCR) = 
[Number of Objectives Completed/Total Number of Objectives Assigned] * 100
"""


@api_view(['GET'])
def objective_completion_rate(request, user_id, start_date, end_date):
    # get the user
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # retrieve all objectives assigned in timeframe
    list_1 = Objective.objects.filter(
        assign_to__id__in=user_id,
        start_date__lte=end_date,
        end_date__gte=start_date
    )
    list_1_count = list_1.count()

    # retrieve all the objectives completed from the assigned ones in the timeframe
    list_2 = Objective.objects.filter(
        assign_to__id__in=user_id,
        status='Completed',
        # objective's deadline is after or on start_date
        deadline__gte=start_date,
        deadline__lte=end_date                # objective's deadline is before or on end_date
    )
    list_2_count = list_2.count()

    # Objective Achievement Rate (OAR)
    if list_1_count > 0:
        ocr = (list_2_count / list_1_count) * 100
    else:
        ocr = 0
    data = {
        'user': UserSerializer(user).data,
        'completed_objectives': list_2,
        'assigned_objectives': list_1,
        'completed_objectives_count': list_2_count,
        'assigned_objectives_count': list_1_count,
        'ocr': ocr
    }

    return Response(data)

# Time to Objective Completion


def time_objective_completion(request, objective_id):
    # get the objective
    try:
        objective = Objective.objects.get(objective_id=objective_id)
    except Objective.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # time to completion
    if objective.completion_date != None:
        toc = objective.completion_date - objective.start_date
    else:
        toc = 0

    data = {'toc': toc}
    return Response(data)

# Number of objectives assigned vs completed


def objective_assigned_completed(request, user_id):
    # get the user
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # retrieve all objectives assigned to the user
    list_1 = Objective.objects.filter(
        assign_to__id__in=user_id)
    list_1_count = list_1.count()

    # retrieve all the objectives completed from the assigned ones
    list_2 = Objective.objects.filter(
        assign_to__id__in=user_id,
        status='Completed',

    )
    list_2_count = list_2.count()

    # Objective Achievement Rate (OAR)
    if list_1_count > 0:
        oac = (list_2_count / list_1_count)
    else:
        oac = 0
    data = {
        'user': UserSerializer(user).data,
        'completed_objectives': list_2,
        'assigned_objectives': list_1,
        'completed_objectives_count': list_2_count,
        'assigned_objectives_count': list_1_count,
        'oac': oac
    }

    return Response(data)

# Ressource Utilization Efficiency (RUE)


def ressouce_utilization_efficiency(request, user_id, start_date, end_date):
    # get all the actions for all the objectives in a period
    # 1  - get the user
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # 2  - retrieve all actions related to objectives in timeframe
    actions = ActionMainEntry.objects.filter(
        objective__start_date__lte=end_date,
        objective__end_date__gte=start_date,
        # if user_id is in the assign_to list
        objective__assign_to__in=[user_id]

    )
    # for all action get the action.duration and sum everything
    duration = 0
    for action in actions:
        duration += action.duration

    objectives = Objective.objects.filter(
        start_date__lte=end_date,
        end_date__gte=start_date,
        assign_to__in=[user_id]
    )
    estimated_hours = 0
    for objective in objectives:
        estimated_hours += objective.estimated_hours

    # divide by the estimated hours for an objective
    rue = (duration/estimated_hours) * 100

    data = {
        'user': UserSerializer(user).data,
        'actions': actions,
        'objectives': objectives,

        'rue': rue
    }
