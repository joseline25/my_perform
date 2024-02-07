from django.shortcuts import render, redirect
from .models import *
from .form import *

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

# create an action


def create_action(request):
    context = {}
    form = ActionForm()
    print(form)
    if request.method == 'POST':
        form = ActionForm(request.POST)
        
        if form.is_valid():
            # now save the form
            new_action = form.save(commit=False)

            collaborators = form.cleaned_data['collaborators']
            tools = form.cleaned_data['tools']


            new_action.collaborators.set(collaborators)
            new_action.tools.set(tools)

            new_action.save()
            print(new_action)
            return redirect('action:list_actions')
        else:
            print(form)
            print(form.errors)
            return redirect('action:list_actions')
    else:
        print(form.errors)
        form = ActionForm()
    # get the kpis of the objective

    context = {'form': form, }

    return render(request, 'action/create.html', context)
