from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import *
# for formset
from django.forms import modelformset_factory


class ObjectiveForm(forms.ModelForm):
    objective_type = forms.ChoiceField(
        choices=Objective.objective_types, widget=forms.RadioSelect)
    complexity = forms.ChoiceField(choices=Objective.complexities)
    priority = forms.ChoiceField(choices=Objective.priorities)
    # Set the queryset to the desired choices
    evaluator = forms.ModelChoiceField(queryset=User.objects.all(), required=False)

    class Meta:
        model = Objective
        # exclude = ['created_at', 'updated_at']
        fields = ['objective_name', 'assign_to', 'visible_to', 'associated_task', 'evaluator','repeat_date',
                  'deadline', 'action_phrase', 'number', 'units', 'start_date',
                  'end_date', 'priority', 'complexity', 'objective_type', 'skills',
                  'tools', 'dog', 'repeat']

        widgets = {
            # format='%Y-%m-%d',
            'deadline': forms.DateInput(attrs={'class': 'form-control italic-placeholder deadline-input', 'placeholder': 'Deadline', 'type': 'date'}),

            'repeat_date': forms.DateInput(attrs={'class': 'form-control form-control-lg italic-placeholder repeat-date', 'placeholder': 'Repeat date', 'type': 'date'}),
            'start_date': forms.DateInput(attrs={'class': ' start-date form-control form-control-lg italic-placeholder', 'placeholder': 'Select a '
                                                 'date',
                                                 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'end-date-input form-control form-control-lg italic-placeholder', 'placeholder': 'Select a '
                                               'date',
                                               'type': 'date'}),
            'objective_name': forms.TextInput(attrs={'placeholder': 'E.g Employ 5 Developers by March'}),
            'action_phrase': forms.TextInput(attrs={'class': 'form-control italic-placeholder action-phrase-input', 'placeholder': 'E.g. Clean, Make'}),
            'number': forms.NumberInput(attrs={'class': 'form-control italic-placeholder number-input', 'placeholder': 'Number', "type": 'number', 'pattern': '[0-9]+', 'title': 'Numbers only'}),
            'units': forms.TextInput(attrs={'class': 'form-control italic-placeholder units-input', 'placeholder': 'E.g. Emails, Notes'}),
            'priority': forms.Select(attrs={'class': 'form-select  form-select-lg italic-placeholder objective-priority'}),
            'complexity': forms.Select(attrs={'class': 'form-select  form-select-lg italic-placeholder objective-complexity'}),
            'dog': forms.CheckboxSelectMultiple (attrs={'class': 'form-select border-0  form-select-lg italic-placeholder',  'placeholder': 'Enter Acceptance Criteria', 'style': 'background-color: #EBEBEB;'}, ),
            'assign_to': forms.CheckboxSelectMultiple (attrs={'class': 'border-0  form-select italic-placeholder option checkbox',  'placeholder': 'Assign To', 'style': 'height: 100px;'}),
            'visible_to': forms.CheckboxSelectMultiple (attrs={'class': 'border-0  form-select italic-placeholder',  'placeholder': 'Visible To', 'style': 'height: 100px;'}),
            'tools': forms.CheckboxSelectMultiple (attrs={'class': 'border-0  form-select italic-placeholder',  'placeholder': 'Assign To', 'style': 'height: 100px;'}),
            'associated_task': forms.CheckboxSelectMultiple (attrs={'class': 'border-0  form-select italic-placeholder',  'placeholder': 'Assign To', 'style': 'height: 100px;'}),
            'evaluator': forms.Select(attrs={'class': 'border-0  form-select italic-placeholder',  'placeholder': 'Assign To', 'style': 'height: 100px;'}),
            'skills': forms.CheckboxSelectMultiple (attrs={'class': 'border-0  form-select italic-placeholder',  'placeholder': 'Assign To', 'style': 'height: 100px;'}),
            # 'choices': Objective.objective_types}
            'objective_type': forms.RadioSelect(attrs={'class': 'radio objective-type', 'type': 'radio', }),
            # 'repeat': forms.RadioSelect(attrs={'class': 'repeat-radio', 'type': 'radio'}),
        }

    # validators

    # Start date not earlier than current date

    def clean_start_date(self):
        start_date = self.cleaned_data['start_date']
        if start_date < timezone.now():
            raise ValidationError("Start date cannot be in the past.")
        return start_date

     # End date not earlier than Start date

    def clean_end_date(self):
        end_date = self.cleaned_data['end_date']
        start_date = self.cleaned_data.get('start_date')
        if start_date and end_date and end_date < start_date:
            raise ValidationError(
                "End date cannot be earlier than the start date.")
        return end_date

   # Definition of Good (dog) cannot be empty
    # def clean_dog(self):
    #     dog = self.cleaned_data['dog']
    #     if not dog:
    #         raise ValidationError(
    #             "Please select at least one option for the dog field.")
    #     return dog


class ObjectiveDraftForm(forms.ModelForm):
    class Meta:
        model = ObjectiveDraft
        fields = ['is_draft']


# in order to create the formset of Objective

class ToolForm(forms.ModelForm):
    class Meta:
        model = Tool
        fields = ['tool_name', 'description', 'teams']


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['skill_name', 'skill_description']


class DefinitionOfGoodForm(forms.Form):
    class Meta:
        model = DefinitionOfGood
        fields = ['dog_criteria']


# import modelformset_factory : from django.forms import modelformset_factory
# then

ObjectiveFormSet = modelformset_factory(
    Objective,
    fields=[
        'objective_type', 'deadline', 'repeat_date', 'start_date', 'end_date',
        'objective_name', 'action_phrase', 'number', 'units', 'priority',
        'complexity', 'assign_to', 'visible_to', 'evaluator'
    ],
    extra=1,  # Number of empty forms to display
)

DefinitionOfGoodFormSet = modelformset_factory(
    DefinitionOfGood,
    form=DefinitionOfGoodForm,
    extra=1,
)

ToolFormSet = modelformset_factory(
    Tool,
    form=ToolForm,
    extra=1,
)

SkillFormSet = modelformset_factory(
    Skill,
    form=SkillForm,
    extra=1,
)


""" 

Each related model (DefinitionOfGood, Tool, Skill) has its own form 
(DefinitionOfGoodForm, ToolForm, SkillForm).
The ObjectiveFormSet is created using modelformset_factory for the
Objective model. The DefinitionOfGoodFormSet, ToolFormSet, and SkillFormSet 
are similarly created for each related model.
"""

# now let's go to the views.py file


# KPI form
class KPIForm(forms.ModelForm):
    class Meta:
        model = KPI
        # exclude = ['created_at', 'updated_at']
        exclude = ['objective']

        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'E.g Employ 5 Developers by March'}),
            'description': forms.TextInput(attrs={'placeholder': 'E.g Clean, Make'}),
            'number': forms.NumberInput(attrs={}),
            'frequency': forms.TextInput(attrs={}),
            'unit': forms.TextInput(attrs={}),
            # 'objective': forms.Select(attrs={'class': 'form-control'}),
        }
