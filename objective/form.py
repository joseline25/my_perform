from django import forms
from .models import *

class ObjectiveForm(forms.ModelForm):
   class Meta:
      model = Objective
      #exclude = ['created_at', 'updated_at']
      # fields = '__all__'
      fields = [
            'assign_to',
            'created_by',
            'associated_task',
            'evaluator',
            'repeat_date',
            'action_phrase',
            'number',
            'units',
            'start_date',
            'end_date',
            'priority',
            'complexity',
            'objective_type',
            'skills',
            'tools',
            'dog',
            'is_draft',
            'repeat',
        ]
      
      widgets = {
            'repeat_date': forms.DateTimeInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'placeholder': 'Select a '
                                                                                                            'date',
                                                                    'type': 'date'}),
            'start_date': forms.DateTimeInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'placeholder': 'Select a '
                                                                                                            'date',
                                                                    'type': 'date'}) ,
            'end_date': forms.DateTimeInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'placeholder': 'Select a '
                                                                                                            'date',
                                                                    'type': 'date'}),

           'action_phrase': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'E.g Clean, Make'}), 
           'number': forms.NumberInput(attrs={'class': 'form-control'}),
           'units': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'E.g Email, Notes'}),
           'priority': forms.Select(attrs={'class': 'form-control'}),
           'complexity': forms.Select(attrs={'class': 'form-control'}),
           'dog': forms.CheckboxSelectMultiple(),
           'assign_to': forms.CheckboxSelectMultiple(),
           'tools': forms.CheckboxSelectMultiple(),
           'associated_task': forms.CheckboxSelectMultiple(),
           'evaluator': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Set who should evaluate this'}),
           'skills': forms.CheckboxSelectMultiple(),
        }
 