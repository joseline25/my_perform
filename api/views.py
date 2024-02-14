from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import ObjectiveSerializer, ObjectiveSerializerPost, ActionSerializer, ActionSerializerPost, TeamSerializer, KPISerializer, KPISerializerPost, QuestionSerializer, ToolSerializer, SkillSerializer, TaskSerializer
from objective.models import Objective, Team, UserTeam, KPI, Tool, Skill
from objective.models_additional.task import Task
from action.models import Action, Question
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework import status
from django.shortcuts import get_object_or_404


# list of objectives

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


# details of one objective


@api_view(['GET'])
def objective_detail(request, objective_id):
    try:
        objective = Objective.objects.get(pk=objective_id)
    except Objective.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ObjectiveSerializer(objective)
    return Response(serializer.data)


# create an objective


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


# update an objective

@api_view(['PUT'])
def update_objective(request, objective_id):
    try:
        objective = Objective.objects.get(pk=objective_id)
    except Objective.DoesNotExist:
        return Response({"message": "No objective found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = ObjectiveSerializerPost(objective, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response({"message": "Objective successfilly updated"}, serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# delete an objective


@api_view(['DELETE'])
def delete_objective(request, objective_id):
    try:
        objective = Objective.objects.get(pk=objective_id)
    except Objective.DoesNotExist:
        return Response({"message": "No Objective found"}, status=status.HTTP_404_NOT_FOUND)

    objective.delete()
    return Response({"message": "This Objective is deleted"}, tatus=status.HTTP_204_NO_CONTENT)


# list of actions
@api_view(['GET'])
def all_actions(request):
    actions = Action.objects.all()
    serializer = ActionSerializer(actions, many=True)
    return Response(serializer.data)

# list of actions for a specific objective


@api_view(["GET"])
def action_objective(request, objective_id):
    try:
        actions = Action.objects.filter(objective=objective_id)

    except Action.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ActionSerializer(actions, many=True)
    return Response(serializer.data)


# action details
@api_view(["GET"])
def action_details(request, id):
    try:
        action = Action.objects.get(pk=id)
    except Action.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ActionSerializer(action)
    return Response(serializer.data)


@api_view(['PUT'])
def update_action(request, pk):
    try:
        action = Action.objects.get(id=pk)
    except Action.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = ActionSerializerPost(action, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({'error': 'Invalid HTTP method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['Delete'])
def delete_action(request, pk):
    try:
        action = Action.objects.get(id=pk)
    except Action.DoesNotExist:
        return Response({"message": "No action found"}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'Delete':
        action.delete()
        return Response({"message": "Action has been deleted"}, status=status.HTTP_204_NO_CONTENT)
    return Response({'error': 'Invalid HTTP method'}, status.HTTP_405_METHOD_NOT_ALLOWED)


# list of questions for an objective


@api_view(['GET'])
def questions(request, objective_id):
    try:
        questions = Question.objects.filter(objective_id=objective_id)
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
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = UserSerializer(user)
    return Response(serializer.data)


# get the users in the same team as a specific user
@api_view(['GET'])
def users_in_same_team(request, user_id):
    try:
        # get the user
        user = User.objects.get(pk=user_id)
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


# get all the kpis
@api_view(['GET'])
def kpis_all(request):
    kpis = KPI.objects.all()
    kpi_serializer = KPISerializer(kpis, many=True)
    return Response(kpi_serializer.data)

# update a kpi


@api_view(['PUT'])
def update_kpi(request, pk):
    try:
        kpi = KPI.objects.get(id=pk)
    except KPI.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        serializer = KPISerializerPost(kpi, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({'error': 'Invalid HTTP method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['DELETE'])
def delete_kpi(request, pk):
    try:
        kpi = KPI.objects.get(id=pk)
    except KPI.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'DELETE':
        kpi.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response({'error': 'Invalid HTTP method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
def all_tools(request):
    tools = Tool.objects.all()
    serializer = ToolSerializer(tools, many=True)
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
        tool = Tool.objects.get(pk=tool_id)
    except Tool.DoesNotExist:
        return Response({"message": "No tool found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = ToolSerializer(tool, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response({"message": "Tool successfilly updated"}, serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_tool(request, tool_id):
    try:
        tool = Tool.objects.get(pk=tool_id)
    except Tool.DoesNotExist:
        return Response({"message": "No Tool found"}, status=status.HTTP_404_NOT_FOUND)

    tool.delete()
    return Response({"message": "This Tool is deleted"}, tatus=status.HTTP_204_NO_CONTENT)


@api_view(['PUT'])
def update_skill(request, skill_id):
    try:
        skill = Skill.objects.get(pk=skill_id)
    except Skill.DoesNotExist:
        return Response({"message": "No skill found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = SkillSerializer(skill, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response({"message": "Skill updated succesfully"}, serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_skill(request, skill_id):
    try:
        skill = Skill.objects.get(pk=skill_id)
    except Skill.DoesNotExist:
        return Response({"message": "No skill found"}, status=status.HTTP_404_NOT_FOUND)

    skill.delete()
    return Response({"message": "Skill deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['PUT'])
def update_user(request, id):
    try:
        user = User.objects.get(pk=id)
    except User.DoesNotExist:
        return Response({"message": "No user found with this id"}, status=status.HTTP_404_NOT_FOUND)

    serializer = UserSerializer(user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User saved successfully"})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_user(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response({"message": "No user found with this id"}, status=status.HTTP_404_NOT_FOUND)
    user.delete()
    return Response({"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['PUT'])
def update_team(request, pk):
    try:
        team = Team.objects.get(pk=pk)
    except Team.DoesNotExist:
        return Response({"message": "Team not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = TeamSerializer(team, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Team updated successfully"}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_team(request, pk):
    try:
        team = Team.objects.get(pk=pk)
    except Team.DoesNotExist:
        return Response({"message": "Team not found"}, status=status.HTTP_404_NOT_FOUND)

    team.delete()
    return Response({"message": "Team deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


{"name": "kpi_1",
 "description": "the first kpis too test the KPI form",
 "number": 3,
 "frequency": "Weekly",
 "unit": 1,
 "objective": 1}
