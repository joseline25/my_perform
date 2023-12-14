from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.contrib import messages
from .form import *
from .models import Objective, ObjectiveDraft, Tool, Skill, DefinitionOfGood

# Create your views here.


# list of objectives
def list_objective(request):
    objectives = Objective.objects.all()
    context = {'objectives': objectives}

    return render(request, 'objective/list_objective.html', context)


# objective details
def details_objective(request, objective_id):
    objective = Objective.objects.get(objective_id=objective_id)
    form = KPIForm()
    print(form)
    if request.method == 'POST':
        form = KPIForm(request.POST)
        print(form)
        if form.is_valid():
            # now save the form
            kpi = form.save(commit=False)
            kpi.objective = objective
            kpi.save()
            return redirect('objective:detail_objective', objective_id=objective_id)
    else:
        print(form.errors)
        form = KPIForm()
    # get the kpis of the objective
    kpis = KPI.objects.filter(objective=objective)
    print('Hi')
    print(kpis)
    context = {'objective': objective, 'form': form, 'kpis': kpis}
    return render(request, 'objective/details_objective.html', context)


# KPI details
def details_kpi(request, id):
    kpi = KPI.objects.get(id=id)
    context = {'kpi': kpi, }
    return render(request, 'objective/details_kpi.html', context)

# objective update


def edit_objective(request, id):
    objective = Objective.objects.get(objective_id=id)
    if request.method == 'POST':
        form = ObjectiveForm(request.POST, instance=objective)
        if form.is_valid():
            # Save the form without committing to the database
            new_objective = form.save(commit=False)

            # # Clear existing many-to-many relationships
            # new_objective.assign_to.clear()
            # new_objective.tools.clear()
            # new_objective.visible_to.clear()
            # new_objective.associated_task.clear()
            # new_objective.skills.clear()
            # new_objective.dog.clear()

            # # Set the new many-to-many relationships
            # new_objective.assign_to.set(form.cleaned_data['assign_to'])
            # new_objective.tools.set(form.cleaned_data['tools'])
            # new_objective.visible_to.set(form.cleaned_data['visible_to'])
            # new_objective.associated_task.set(
            #     form.cleaned_data['associated_task'])
            # new_objective.skills.set(form.cleaned_data['skills'])
            # new_objective.dog.set(form.cleaned_data['dog'])

            # Compare cleaned data with current values
            if set(form.cleaned_data['assign_to']) != set(objective.assign_to.all()):
                new_objective.assign_to.clear()
                new_objective.assign_to.add(*form.cleaned_data['assign_to'])

            if set(form.cleaned_data['tools']) != set(objective.tools.all()):
                new_objective.tools.clear()
                new_objective.tools.add(*form.cleaned_data['tools'])

            if set(form.cleaned_data['visible_to']) != set(objective.visible_to.all()):
                new_objective.visible_to.clear()
                new_objective.visible_to.add(*form.cleaned_data['visible_to'])

            if set(form.cleaned_data['associated_task']) != set(objective.associated_task.all()):
                new_objective.associated_task.clear()
                new_objective.associated_task.add(
                    *form.cleaned_data['associated_task'])

            if set(form.cleaned_data['skills']) != set(objective.skills.all()):
                new_objective.skills.clear()
                new_objective.skills.add(*form.cleaned_data['skills'])

            if set(form.cleaned_data['dog']) != set(objective.dog.all()):
                new_objective.dog.clear()
                new_objective.dog.add(*form.cleaned_data['dog'])

            new_objective.save()

            return redirect('objective:list_objective')
    else:
        form = ObjectiveForm(instance=objective)

    context = {'form': form, 'objective': objective, 'edit_mode': True}
    return render(request, 'objective/create_objective.html', context)


# create an objective with Che's form
def create_objective(request):

    context = {}

    if request.method == 'GET':
        form = ObjectiveForm()
        draft_form = ObjectiveDraftForm()
        context['form'] = form
        context['draft_form'] = draft_form
        return render(request, 'objective/create_objective.html', context)

    elif request.method == "POST":
        form = ObjectiveForm(request.POST)
        # for draft
        draft_form = ObjectiveDraftForm(request.POST)
        submit_action = request.POST.get('submit_action', None)
        if form.is_valid() and draft_form.is_valid():
            # form.save()
            # create a new Objective instance without saving it to the database immediately.
            new_objective = form.save(commit=False)

            # Proceed field
            assign_to = form.cleaned_data['assign_to']
            visible_to = form.cleaned_data['visible_to']
            associated_task = form.cleaned_data['associated_task']
            evaluator = form.cleaned_data['evaluator']
            repeat_date = form.cleaned_data['repeat_date']
            action_phrase = form.cleaned_data['action_phrase']
            number = form.cleaned_data['number']
            units = form.cleaned_data['units']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            priority = form.cleaned_data['priority']
            complexity = form.cleaned_data['complexity']
            objective_type = form.cleaned_data['objective_type']
            skills = form.cleaned_data['skills']
            tools = form.cleaned_data['tools']
            dog = form.cleaned_data['dog']
            is_draft = form.cleaned_data['is_draft']
            repeat = form.cleaned_data['repeat']
            deadline = form.cleaned_data['deadline']
            # save
            if submit_action == 'save':
                # Save the form normally
                new_objective.save()
                return redirect('objective:list_objective')
            elif submit_action == 'save_as_draft':

                # Set the is_draft field for the original objective and save it
                new_objective.is_draft = True
                new_objective.save()
                # Save the draft form in the DraftObjective table
                draft_objective = draft_form.save(commit=False)
                draft_objective.objective = new_objective
                draft_objective.save()

                return redirect('objective:list_objective')

            # proceed Many to Many fields
            # assign the selected authors to the ManyToManyField using the set() method
            new_objective.assign_to.set(assign_to)
            new_objective.visible_to.set(visible_to)
            new_objective.associated_task.set(associated_task)
            new_objective.skills.set(skills)
            new_objective.tools.set(tools)
            new_objective.dog.set(dog)
            print(new_objective)

            return redirect('objective:list_objective')
        else:
            print(form)
            print(form.errors)
            return redirect('objective:create_objective')

    else:
        messages.error("Please correct the following errors")
        return render(request, 'objective/create_objective.html', context)


# create an objective with Abdulrahim's form
def create_objective_two(request):

    context = {}

    if request.method == 'GET':
        print('here')
        form = ObjectiveForm()
        draft_form = ObjectiveDraftForm()
        context['form'] = form
        context['draft_form'] = draft_form
        return render(request, 'objective/create_objective_two.html', context)

    elif request.method == "POST":
        form = ObjectiveForm(request.POST)
        # for draft
        draft_form = ObjectiveDraftForm(request.POST)
        submit_action = request.POST.get('submit_action', None)
        if form.is_valid() and draft_form.is_valid():
            # form.save()
            print(form)
            # create a new Objective instance without saving it to the database immediately.
            new_objective = form.save(commit=False)

            # Proceed field
            assign_to = form.cleaned_data['assign_to']
            visible_to = form.cleaned_data['visible_to']
            associated_task = form.cleaned_data['associated_task']
            evaluator = form.cleaned_data['evaluator']
            repeat_date = form.cleaned_data['repeat_date']
            action_phrase = form.cleaned_data['action_phrase']
            number = form.cleaned_data['number']
            units = form.cleaned_data['units']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            priority = form.cleaned_data['priority']
            complexity = form.cleaned_data['complexity']
            objective_type = form.cleaned_data['objective_type']
            skills = form.cleaned_data['skills']
            tools = form.cleaned_data['tools']
            dog = form.cleaned_data['dog']
            
            repeat = form.cleaned_data['repeat']
            deadline = form.cleaned_data['deadline']
            # save
            if submit_action == 'save':
                # Save the form normally
                new_objective.save()
                return redirect('objective:list_objective')
            elif submit_action == 'save_as_draft':

                # Set the is_draft field for the original objective and save it
                new_objective.is_draft = True
                new_objective.save()
                # Save the draft form in the DraftObjective table
                draft_objective = draft_form.save(commit=False)
                draft_objective.objective = new_objective
                draft_objective.save()

                return redirect('objective:list_objective')

            # proceed Many to Many fields
            # assign the selected authors to the ManyToManyField using the set() method
            new_objective.assign_to.set(assign_to)
            new_objective.visible_to.set(visible_to)
            new_objective.associated_task.set(associated_task)
            new_objective.skills.set(skills)
            new_objective.tools.set(tools)
            new_objective.dog.set(dog)
            print(new_objective)

            return redirect('objective:list_objective')
        else:
            print(form)
            print(form.errors)
            return redirect('objective:create_objective_two')

    else:
        messages.error("Please correct the following errors")
        return render(request, 'objective/create_objective_two.html', context)


# kpi edit
def edit_kpi(request, id, objective_id):
    kpi = KPI.objects.get(id=id)
    objective = Objective.objects.get(objective_id=objective_id)
    if request.method == 'POST':
        form = KPIForm(request.POST, instance=kpi)
        if form.is_valid():
            # Save the form
            form.save()
            redirect('objective:detail_objective', objective_id=objective_id)
    else:
        form = KPIForm(instance=kpi)

    context = {'form': form, 'objective': objective, 'edit_mode': True}
    return render(request, 'objective/details_objective.html', context)


