# create a formset for objectives and models : DefinitionOfGood, Tool, Skill

def create_objective_with_related(request):
    context = {}
    # the prefix parameter is used to set a unique identifier for the formset
    if request.method == 'POST':
        objective_formset = ObjectiveFormSet(request.POST, prefix='objectives')
        definition_of_good_formset = DefinitionOfGoodFormSet(
            request.POST, prefix='dog')
        tool_formset = ToolFormSet(request.POST, prefix='tools')
        skill_formset = SkillFormSet(request.POST, prefix='skills')

        if (
            objective_formset.is_valid() and
            definition_of_good_formset.is_valid() and
            tool_formset.is_valid() and
            skill_formset.is_valid()
        ):

            # Save each formset
            objective_instances = objective_formset.save()
            definition_of_good_instances = definition_of_good_formset.save()
            tool_instances = tool_formset.save()
            skill_instances = skill_formset.save()

            # Since we have ForeignKey or ManyToManyField relationships
            for objective_instance in objective_instances:
                objective_instance.definition_of_good.set(
                    definition_of_good_instances)
                objective_instance.tools.set(tool_instances)
                objective_instance.skills.set(skill_instances)

    else:
        objective_formset = ObjectiveFormSet(prefix='objectives')
        definition_of_good_formset = DefinitionOfGoodFormSet(
            prefix='good_objects')
        tool_formset = ToolFormSet(prefix='tools')
        skill_formset = SkillFormSet(prefix='skills')

    return render(
        request,
        'objective/create_formset.html',
        {
            'objective_formset': objective_formset,
            'definition_of_good_formset': definition_of_good_formset,
            'tool_formset': tool_formset,
            'skill_formset': skill_formset,
        }
    )


# Che's form

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
            print(form)
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
            # is_draft = form.cleaned_data['is_draft']
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

            new_objective.save()
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
