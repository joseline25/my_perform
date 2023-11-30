from django import forms
from .models import *

class ObjectiveForm(forms.ModelForm):
   class Meta:
      model = Objective
      #exclude = ['created_at', 'updated_at']
      fields = '__all__'
      
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
            
        }
 

 # Duration Validation (Start & End Date)

from django.utils import timezone

class YourDateRangeForm(forms.Form):
    startdate = forms.DateField()
    enddate = forms.DateField()

    def clean(self):
        cleaned_data = super().clean()
        startdate = cleaned_data.get("startdate")
        enddate = cleaned_data.get("enddate")
        current_date = timezone.now().date()

        # Check if startdate is provided
        if not startdate:
            raise forms.ValidationError("Start date field cannot be left empty.")

        # Check if enddate is provided
        if not enddate:
            raise forms.ValidationError("End date field cannot be left empty.")

        # Check if enddate is less than startdate
        if enddate < startdate:
            raise forms.ValidationError("End date cannot be less than start date.")

        # Check if enddate is before the current date
        # if enddate < current_date:
        #     raise forms.ValidationError("End date cannot be before the current date.")

        return cleaned_data


# Validation of Definition of Good form field
class Yourdog(forms.Form):
    dog = forms.CharField()

    def clean_dog(self):
        data = self.cleaned_data['dog']

        if not data:
            raise forms.ValidationError("The 'dog' field cannot be left empty.")

        return data

# Validation of Visible-to form field
class YourVisibleTo(forms.Form):
    visibleTo = forms.CharField()

    def clean_visibleTo(self):
        data = self.cleaned_data['visibleTo']

        if not data:
            raise forms.ValidationError("The 'visible to' field cannot be left empty.")

        return data


# Validation of Visible-to form field
class Your(forms.Form):
    assignTo = forms.CharField()

    def clean_visibleTo(self):
        data = self.cleaned_data['assignTo']

        if not data:
            raise forms.ValidationError("The 'assign to' field cannot be left empty.")

        return data


# Validation of Evaluator form field
class YourEvaluator(forms.Form):
    evaluator = forms.CharField()

    def clean_visibleTo(self):
        data = self.cleaned_data['evaluator']

        if not data:
            raise forms.ValidationError("The 'evaluator' field cannot be left empty.")

        return data
    

from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone

class YourModelRepeatDate(models.Model):
    # Other fields in your model

    repeat_date = models.DateField(
        validators=[MinValueValidator(limit_value=timezone.now().date())],
        # Other attributes for your field
    )

   
