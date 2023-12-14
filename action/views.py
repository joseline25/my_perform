from django.shortcuts import render
from .models import *
from django.views import View
from .models import Actions
from .form import ActionForm

# Create your views here.

class ActionView(View):
    def post(self, request):
        form = ActionForm(request.POST)
        if form.is_valid():
            form.save()
            return True
        else:
            return False    
    
# list of actions

def list_actions(request):
    actions = Action.objects.all()
    context = {'actions': actions}
    return render(request, 'action/list_actions.html', context)


def details_action(request, id):
    action = Action.objects.get(id=id)
    context = {'action': action}
    return render(request, 'action/details_action.html', context)