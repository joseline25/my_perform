from django import forms
from .models import *

class ObjectiveForm(forms.ModelForm):
   class Meta:
      model = Objective
      #exclude = ['created_at', 'updated_at']
      fields = '__all__'
      
      widgets = {
            'start_date': forms.DateTimeInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'placeholder': 'Select a '
                                                                                                            'date',
                                                                    'type': 'date'}) ,
            'end_date': forms.DateTimeInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'placeholder': 'Select a '
                                                                                                            'date',
                                                                    'type': 'date'}),
        }
 