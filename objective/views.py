from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import CreateView
from django.contrib import messages
from .form import *
from .models import Objective

# Create your views here.


# list of objectives
def list_objective(request):
    objectives = Objective.objects.all()
    context = {'objectives': objectives}
    return render(request, 'objective/list_objective.html', context)


# objective update
def edit_objective(request, id):
    objective = Objective.objects.get(id=id)
    form = ObjectiveForm(instance=objective)

    if request.method == 'POST':
        form = ObjectiveForm(request.POST, instance=objective)
        if form.is_valid():
            form.save()
            return redirect('list_objective')

    context = {'form': form}
    return render(request, 'objective/create_objective.html', context)


# create an objective
def create_objective(request):

    context = {}

    if request.method == 'GET':
        context['form'] = ObjectiveForm()
        return render(request, 'objective/create_objective.html', context)

    elif request.method == "POST":
        form = ObjectiveForm(request.POST)
        if form.is_valid():
            form.save()
            # messages.success("Objective created!")
            return redirect('list_objective')

    else:
        messages.error("Please correct the following errors")
        return render(request, 'objective/create_objective.html', context)

# view single objective
def view_objective(request, pk):
    objective = get_object_or_404(Objective, objective_id=pk)
    context = {'objective': objective}
    return render(request, 'objective/view_objective.html', context)