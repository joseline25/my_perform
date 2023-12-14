from django.shortcuts import render
from .models import *

# Create your views here.

# list of actions

def list_actions(request):
    actions = Action.objects.all()
    context = {'actions': actions}
    return render(request, 'action/list_actions.html', context)


def details_action(request, id):
    action = Action.objects.get(id=id)
    context = {'action': action}
    return render(request, 'action/details_action.html', context)