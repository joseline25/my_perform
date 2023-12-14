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
