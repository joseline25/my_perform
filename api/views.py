from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import ObjectiveSerializer, ActionSerializer, TeamSerializer, QuestionSerializer
from objective.models import Objective, Team, UserTeam
from action.models import Action, Question

from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework import status






# list of objectives


@api_view(['GET'])
def all_objectives(request):
    objectives = Objective.objects.all()
    serializer = ObjectiveSerializer(objectives, many=True)
    return Response(serializer.data)



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
        serializer.save()
        print(serializer.data)
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# list of actions
@api_view(['GET'])
def all_actions(request):
    actions = Action.objects.all()
    serializer = ActionSerializer(actions, many=True)
    return Response(serializer.data)

#list of actions for a specific objective 
@api_view(["GET"])
def action_objective(request, objective_id):
    try:
        actions = Action.objects.filter(objective=objective_id)

    except Action.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = ActionSerializer(actions, many=True)
    return Response(serializer.data)


#action details
@api_view(["GET"])
def action_details(request, id):
    try:
        action = Action.objects.get(pk=id)
    except Action.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = ActionSerializer(action)
    return Response(serializer.data)

#list of questions for an objective
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
        users_in_same_team = User.objects.filter(userteam__team__in=user_teams).exclude(id=user_id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = UserSerializer(users_in_same_team, many=True)
    return Response(serializer.data)