from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import ObjectiveSerializer, ActionSerializer, TeamSerializer, KPISerializer
from objective.models import Objective, Team, UserTeam, KPI
from action.models import Action
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework import status
from django.shortcuts import get_object_or_404


# list of objectives

@api_view(['GET'])
def all_objectives(request):
    objectives = Objective.objects.all()
    objectives_serializer = ObjectiveSerializer(objectives, many=True)

    users = User.objects.values('username', 'first_name', 'last_name', 'email')
    users_serializer = UserSerializer(users, many=True)

    response_data = {
        'objectives': objectives_serializer.data,
        'users': users_serializer.data
    }

    return Response(response_data)

# creation du endpoint qui est l'url dans urls.py

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
    serializer = ObjectiveSerializer(data=request.data)
    if serializer.is_valid():

        print("Validated Data:", serializer.validated_data)

        # save
        new_objective = serializer.save()

        # many to many fields
        new_objective.assign_to.set(serializer.validated_data.get('assign_to'))
        new_objective.visible_to.set(
            serializer.validated_data.get('visible_to'))
        new_objective.associated_task.set(
            serializer.validated_data.get('associated_task'))
        # if 'skills' in serializer.validated_data:
        #     new_objective.skills.set(serializer.validated_data['skills'])
        # if 'tools' in serializer.validated_data:
        #     new_objective.tools.set(serializer.validated_data.get('tools'))

        new_objective.skills.set(serializer.validated_data.get('skills'))
        new_objective.tools.set(serializer.validated_data.get('tools'))
        # new_objective.dog.set(serializer.validated_data.get('dog'))

        return Response({'status': 'success', 'message': 'Objective created successfully'}, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# list of actions
@api_view(['GET'])
def all_actions(request):
    actions = Action.objects.all()
    serializer = ActionSerializer(actions, many=True)
    return Response(serializer.data)

# create an action


@api_view(['POST'])
def create_action(request):
    serializer = ActionSerializer(data=request.data)
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

# @api_view(['GET', 'POST'])
# def kpi_list_create(request, objective_id):
#     objective = get_object_or_404(Objective, objective_id=objective_id)

#     if request.method == 'GET':
#         kpis = KPI.objects.filter(objective=objective)
#         serializer = KPISerializer(kpis, many=True)
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         serializer = KPISerializer(data=request.data)

#         if serializer.is_valid():
#             serializer.save(objective=objective)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
        serializer = KPISerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(objective=objective)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# create a kpi indepedently
@api_view(['POST'])
def create_kpi(request):
    serializer = KPISerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


# get all the kpis
@api_view(['GET'])
def kpis_all(request):
    kpis = KPI.objects.all()
    kpi_serializer = KPISerializer(kpis, many=True)
    return Response(kpi_serializer.data)


{"name": "kpi_1",
 "description": "the first kpis too test the KPI form",
 "number": 3,
 "frequency": "Weekly",
 "unit": 1,
 "objective": 1}
